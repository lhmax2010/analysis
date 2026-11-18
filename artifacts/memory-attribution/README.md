# Normal-board memory attribution

[Verified] One read-only snapshot on the normal-memory KantSU2E yielded 121 process rollups with a combined 557,373 KiB PSS. A follow-up read of smaps for the top 20 processes classified VMAs by backing into 209,614 KiB named file PSS, 112,486 KiB anonymous PSS and 27,691 KiB device/shared/other PSS. The samples were taken at different instants. Actual playback and steady state were unverified. Sizes are KiB.

- [Process rollups](normal-board-rollup-20261117.csv) include PSS/USS and swap.
- [Top-20 mapping buckets](normal-board-mapping-buckets.csv) contain clean and dirty private bytes, plus PSS.
- [Top mapped product files](normal-board-top-file-mappings.csv) aggregate per file basename for the top mapping subset.
- [System memory and CMA](../evidence/board-memory-map-20261117.txt) includes slab and zones.

D-017 requires four finer attributions. During matched playback, join each mapped file, offset and permissions to the actual ELF PT_LOAD and PT_GNU_RELRO ranges. Attribute file-backed clean code/rodata to executable and read-only segment mappings. Treat relocation-dirty pages as estimates where the VMA contains RELRO/GOT, using a matched startup/steady comparison and segment evidence. Private_Dirty on a named mapping also includes written program data. Track anonymous heap/stack independently. Capture Slab, zram and unique CMA/dma-buf counters without summing aliases or adding memory already represented in PSS. A process PSS aggregate cannot identify physical media buffers outside user VMAs. [Linux proc counters](https://docs.kernel.org/filesystems/proc.html)

The first controlled run needs the same stream/player and timestamped playback phase. Pair prelink-enabled and prelink-disabled images only after source, flags, file content scope and runtime state can be controlled. Current data cannot establish a vdprelink causal change.

Round 0003 prioritizes a system-wide playback estimate. Join each file-backed VMA to exact ELF file offsets/build identities and RELRO/GOT/data ranges. Aggregate page-weighted PSS or deduplicate physical pages where identifiable. Report raw private dirty separately and carry uncertainty for adjacent application-writable pages. A named mapping alone cannot distinguish loader relocations from later writes.
