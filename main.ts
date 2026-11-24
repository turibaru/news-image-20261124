// Entry point for news-image-20261124 (round 1).
// Copy-only: copies the pre-rendered entry.png next to this file into
// $MAKEFUN_OUTPUT_DIR/entry.png. No rendering, no network, no writes
// to the repository. Node 22 standard library only.
import { copyFileSync } from "node:fs";
import { join } from "node:path";

const src = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(src, join(outDir, "entry.png"));
