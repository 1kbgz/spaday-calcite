const PYODIDE_VERSION = "314.0.4";
const requestedExample = new URL(self.location.href).searchParams.get(
  "example",
);
const exampleName = requestedExample === "gallery" ? "gallery" : "example";
let pyodide;

const ready = (async () => {
  self.postMessage({ type: "status", message: "Loading Pyodide…" });
  const { loadPyodide } = await import(
    `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.mjs`
  );
  pyodide = await loadPyodide();
  await pyodide.loadPackage(["micropip", "anyio"]);

  self.postMessage({ type: "status", message: `Installing ${exampleName}…` });
  const response = await fetch(new URL("./wheels.json", self.location.href));
  if (!response.ok)
    throw new Error(`wheel manifest returned ${response.status}`);
  const wheels = await response.json();
  const urls = Object.fromEntries(
    Object.entries(wheels).map(([name, path]) => [
      name,
      new URL(path, self.location.href).href,
    ]),
  );
  pyodide.globals.set("wheels_json", JSON.stringify(urls));
  pyodide.globals.set("example_name", exampleName);
  return pyodide.runPythonAsync(`
import importlib
import json
import micropip

wheels = json.loads(wheels_json)
await micropip.install([wheels["spaday"], "starlette"])
await micropip.install(wheels["calcite"], deps=False)

example = importlib.import_module(f"spaday_calcite.{example_name}")

json.dumps({
    "tree": example.page.to_node(),
    "style": example.styles,
    "store": {},
})
`);
})();

let queue = Promise.resolve();

async function handle(message) {
  const snapshot = await ready;
  if (message.type === "start") {
    self.postMessage({ type: "snapshot", payload: JSON.parse(snapshot) });
  }
}

self.addEventListener("message", (event) => {
  queue = queue
    .then(() => handle(event.data))
    .catch((error) => {
      self.postMessage({ type: "error", message: String(error) });
    });
});
