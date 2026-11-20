// Minimal Knowledge Graph for Testing
// Using only English characters to avoid encoding issues

export const DATA = {
  "nodes": [
    {"id": "mindset", "label": "Mindset (rozwojowe vs stale)", "kind": "term", "day": 4, "week": 1, "summary": "Fixed mindset vs growth mindset theory", "example": "Example text here"},
    {"id": "persistence", "label": "Persistence (Wytrwalosc)", "kind": "concept", "day": 4, "week": 1, "summary": "Persisting despite difficulties", "example": ""},
    {"id": "dweck", "label": "Carol Dweck", "kind": "person", "day": null, "week": 1, "summary": "Growth mindset researcher", "example": ""}
  ],
  "edges": [
    {"source": "mindset", "relation": "predicts", "target": "persistence", "basis": "stated"},
    {"source": "dweck", "relation": "author", "target": "mindset", "basis": "stated"}
  ]
};

export function createGraph(canvas, options = {}) {
  console.log("createGraph called with options:", options);
  console.log("DATA loaded:", DATA.nodes.length, "nodes");

  // Minimal implementation for testing
  const ctx = canvas.getContext('2d');

  // Draw something simple to show it works
  ctx.fillStyle = '#fff3e4';
  ctx.font = '20px Arial';
  ctx.fillText('Knowledge Graph Loading...', 50, 50);
  ctx.fillText(`Nodes: ${DATA.nodes.length}`, 50, 90);
  ctx.fillText('Full implementation coming...', 50, 130);

  return {
    select: (id) => console.log('Select:', id),
    setArticle: (ids) => console.log('Set article:', ids),
    setFilter: (f) => console.log('Set filter:', f),
    zoom: (f) => console.log('Zoom:', f),
    destroy: () => console.log('Destroy')
  };
}
