import { bundle } from "./tools/bundle.mjs";
import { bundle_css } from "./tools/css.mjs";

import cpy from "cpy";
import fs from "fs";

const manifest = JSON.parse(
  fs.readFileSync("../spaday_calcite/custom-elements.json", "utf8"),
);
const tags = manifest.modules
  .flatMap((module) =>
    module.declarations.map((declaration) => declaration.tagName),
  )
  .filter(Boolean);
const imports = manifest.modules
  .map((module) => `import "${module.path}";`)
  .join("\n");
const version = JSON.parse(
  fs.readFileSync("node_modules/@esri/calcite-components/package.json", "utf8"),
).version;

const entry = {
  contents: `${imports}\nObject.defineProperty(globalThis, "__spadayCalcite", { value: Object.freeze({ version: ${JSON.stringify(
    version,
  )}, tags: ${JSON.stringify(tags)} }), configurable: true });\n`,
  resolveDir: ".",
  loader: "js",
};

async function build() {
  fs.rmSync("dist", { recursive: true, force: true });
  fs.rmSync("../spaday_calcite/extension", { recursive: true, force: true });

  await bundle_css("src/css/calcite.css");
  await cpy("src/html/*", "dist/");
  await Promise.all([
    bundle({ stdin: entry, outfile: "dist/esm/index.js" }),
    bundle({ stdin: entry, outfile: "dist/cdn/index.js" }),
  ]).catch(() => process.exit(1));

  fs.writeFileSync(
    "dist/versions.json",
    `${JSON.stringify({ "@esri/calcite-components": version }, null, 2)}\n`,
  );
  fs.mkdirSync("../spaday_calcite/extension", { recursive: true });
  await cpy("dist/**/*", "../spaday_calcite/extension", {
    filter: (file) =>
      !file.relativePath.startsWith("esm/") &&
      !file.relativePath.startsWith("dist/esm/"),
  });
}

await build();
