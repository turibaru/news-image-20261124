// main.ts -- entrypoint for make.fun bounty news-image-20261124 (round 2).
// Copies the pre-rendered entry.png next to this file into
// MAKEFUN_OUTPUT_DIR/entry.png. No network, no DOM. Exits non-zero on
// any failure (missing output dir, missing source file, failed write).
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

const src = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
if (!existsSync(src)) {
  console.error(`source entry.png not found: ${src}`);
  process.exit(1);
}

try {
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  copyFileSync(src, dest);
  if (!existsSync(dest)) {
    console.error(`failed to write ${dest}`);
    process.exit(1);
  }
  console.log(`copied entry.png -> ${dest}`);
} catch (err) {
  console.error(`failed to copy entry.png: ${err}`);
  process.exit(1);
}
