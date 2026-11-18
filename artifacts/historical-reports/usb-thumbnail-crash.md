**USB Video Thumbnail Crash**

**Issue.** Opening a USB video folder can crash `native-home` during thumbnail generation. The media interface becomes unavailable or returns to HomeUI. The failure is a `SIGSEGV` in `libavformat.so`, inside `ff_seek_frame_binary()`.

**Reproduction.**

1. Connect a USB drive containing the affected sample, `48523_VID_[41][CG]Bolt.ts`.
2. From HomeUI, open the USB drive and navigate to the folder containing the sample.
3. Allow video thumbnails to load. Thumbnail extraction seeks approximately two seconds into the video; manually starting playback is not required to trigger this path.
4. Observe the `native-home` crash while the thumbnail is being generated.

The sample is an MPEG-TS file. The relevant trigger is the seek path that bypasses the cached index or encounters a missing index; reproduction depends on the media and index state.

**Root cause.** In `ff_seek_frame_binary()`, the lower and upper position bounds are declared as:

```c
int64_t av_uninit(pos_min), av_uninit(pos_max), pos, pos_limit;
```

In the affected source, `av_uninit(x)` expands to `x = x`. It does not provide a defined initial value. When the index path is bypassed, or an individual cached bound is unavailable, `pos_min` or `pos_max` can remain uninitialized before being passed by value to `ff_gen_search()`.

Reading these indeterminate values is undefined behavior. In the affected optimized Clang binary, the existing MPEG-TS bypass and index-null checks were eliminated. Execution entered the index path with a null index pointer and subsequently accessed invalid index storage, causing the crash. The log immediately preceding the fault reports:

```text
ff_index_search_timestamp: key is NULL
```

This is a source-level undefined-behavior defect exposed by optimization. The observed GCC binary retained the checks, but that behavior does not make the uninitialized reads valid.

**Correction.** Explicitly initialize both position bounds in `gst-libs/ext/ffmpeg/libavformat/utils.c`:

```diff
-    int64_t av_uninit(pos_min), av_uninit(pos_max), pos, pos_limit;
+    int64_t pos_min = 0, pos_max = 0, pos, pos_limit;
```

This supplies defined arguments to `ff_gen_search()`. When a timestamp bound is unknown, the search implementation assigns the corresponding actual position before using it, or returns on failure. When a timestamp bound is known, its position is assigned from a valid index entry. The initialization therefore preserves valid seek behavior, the existing MPEG-TS handling and the public ABI. Target code generated from the corrected source retains the bypass and null-index checks.

**Validation.**

- ARM package builds passed with GCC and Clang.
- Target disassembly confirms that the MPEG-TS bypass and null-index guards are retained.
- The corrected Clang library preserves dynamic symbols and dependencies; neither corrected library contains text relocations.
- Host seek regression tests with modeled I/O passed, covering cached and missing bounds, forward and backward searches, and error paths.
- Television testing passed USB navigation, thumbnail loading, video playback, forward/backward seeking, returning to the file list and reopening playback. HomeUI and the video player were confirmed to load the corrected library.

The targeted regression is resolved. Long-term stability testing and television runtime validation of the GCC build remain pending.
