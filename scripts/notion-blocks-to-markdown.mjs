import fs from "node:fs";

const [input, pageId, output] = process.argv.slice(2);
if (!input || !pageId || !output) {
  throw new Error("Usage: node scripts/notion-blocks-to-markdown.mjs <record-map.json> <page-id> <output.md>");
}

const payload = JSON.parse(fs.readFileSync(input, "utf8"));
const blocks = payload.recordMap?.block || {};
const value = id => {
  const record = blocks[id];
  return record?.value?.value || record?.value || record;
};
const root = value(pageId);
if (!root || root.type !== "page") throw new Error(`Notion page ${pageId} was not found`);

const rich = segments => {
  let result = "", code = "";
  const flushCode = () => {
    if (!code) return;
    result += `\`${code.replaceAll("`", "\\`")}\``;
    code = "";
  };
  for (const [raw, marks = []] of segments || []) {
    let text = String(raw ?? "").replaceAll("|", "\\|").replaceAll("\n", "<br>");
    if (marks.some(mark => mark[0] === "c")) {
      code += text;
      continue;
    }
    flushCode();
    for (const mark of marks) {
      if (mark[0] === "b") text = `**${text}**`;
      if (mark[0] === "i") text = `*${text}*`;
      if (mark[0] === "a" && mark[1]) text = `[${text}](${mark[1]})`;
    }
    result += text;
  }
  flushCode();
  return result;
};

function render(id) {
  const block = value(id);
  if (!block) return "";
  const title = rich(block.properties?.title);
  switch (block.type) {
    case "header": return `## ${title}`;
    case "sub_header": return `### ${title}`;
    case "sub_sub_header":
    case "header_4": return `#### ${title}`;
    case "text": return title;
    case "bulleted_list": return `- ${title}`;
    case "numbered_list": return `1. ${title}`;
    case "divider": return "---";
    case "page": return `- [${title}](local:${block.id})`;
    case "table": {
      const columns = block.format?.table_block_column_order || [];
      const rows = (block.content || []).map(rowId => {
        const row = value(rowId);
        return columns.map(column => rich(row?.properties?.[column]));
      });
      if (!rows.length) return "";
      const header = rows[0];
      return [
        `| ${header.join(" | ")} |`,
        `| ${header.map(() => "---").join(" | ")} |`,
        ...rows.slice(1).map(row => `| ${row.join(" | ")} |`)
      ].join("\n");
    }
    default: return title;
  }
}

const pageTitle = rich(root.properties?.title) || "Notion Page";
const markdown = [`# ${pageTitle}`, "", ...(root.content || []).flatMap(id => [render(id), ""])].join("\n").replace(/\n{3,}/g, "\n\n").trim() + "\n";
fs.writeFileSync(output, markdown, "utf8");
console.log(`Converted ${root.content?.length || 0} Notion blocks to ${output}`);
