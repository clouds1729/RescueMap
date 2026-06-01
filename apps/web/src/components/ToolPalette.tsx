import { Building2, DoorOpen, Flame, MousePointer2, Route, ShieldAlert, Square, Trash2, Waypoints } from "lucide-react";
import type React from "react";
import type { Tool } from "../lib/drawing";

const tools: { id: Tool; label: string; icon: React.ReactNode }[] = [
  { id: "select", label: "Select", icon: <MousePointer2 size={16} /> },
  { id: "wall", label: "Wall", icon: <Waypoints size={16} /> },
  { id: "room", label: "Room", icon: <Square size={16} /> },
  { id: "door", label: "Door", icon: <DoorOpen size={16} /> },
  { id: "exit", label: "Exit", icon: <Route size={16} /> },
  { id: "stairwell", label: "Stairwell", icon: <Building2 size={16} /> },
  { id: "hazard", label: "Hazard", icon: <Flame size={16} /> },
  { id: "restricted_area", label: "Restricted", icon: <ShieldAlert size={16} /> },
  { id: "route_start", label: "Route Start", icon: <Route size={16} /> }
];

export default function ToolPalette({ activeTool, onTool, onDelete }: { activeTool: Tool; onTool: (tool: Tool) => void; onDelete: () => void }) {
  return (
    <section className="panel">
      <h2>Tools</h2>
      <div className="tool-grid">
        {tools.map((tool) => (
          <button key={tool.id} className={activeTool === tool.id ? "tool active" : "tool"} onClick={() => onTool(tool.id)} title={tool.label}>
            {tool.icon}
            <span>{tool.label}</span>
          </button>
        ))}
      </div>
      <button className="danger" onClick={onDelete}>
        <Trash2 size={16} /> Delete Selected
      </button>
    </section>
  );
}
