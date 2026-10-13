import { useState } from "react";
import {
  BookOpen,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  FileText,
} from "lucide-react";

import type { Citation as CitationType } from "../../types";
import { truncate } from "../../utils/formatters";

interface CitationProps {
  citation: CitationType;
  index: number;
}

export default function Citation({
  citation,
  index,
}: CitationProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <article className="citation-card">
      <button
        type="button"
        className="citation-header"
        onClick={() => setExpanded((value) => !value)}
        aria-expanded={expanded}
      >
        <span className="citation-number">{index + 1}</span>

        <span className="citation-file-icon">
          <FileText size={17} />
        </span>

        <span className="citation-info">
          <strong>{citation.filename}</strong>
          <small>
            Chunk {citation.chunk_index + 1}
            {citation.page != null ? ` · Page ${citation.page}` : ""}
          </small>
        </span>

        {citation.score != null && (
          <span className="citation-score">
            {Math.round(citation.score * 100)}%
          </span>
        )}

        {expanded ? (
          <ChevronUp size={16} />
        ) : (
          <ChevronDown size={16} />
        )}
      </button>

      {!expanded && (
        <p className="citation-preview">
          {truncate(citation.text, 180)}
        </p>
      )}

      {expanded && (
        <div className="citation-expanded">
          <div className="citation-source-label">
            <BookOpen size={14} />
            Retrieved source excerpt
          </div>

          <p>{citation.text}</p>

          <div className="citation-footer">
            <span>
              Source ID: {citation.chunk_id.slice(0, 12)}
            </span>

            <button
              type="button"
              className="text-button"
              onClick={() => {
                void navigator.clipboard.writeText(citation.text);
              }}
            >
              <ExternalLink size={13} />
              Copy excerpt
            </button>
          </div>
        </div>
      )}
    </article>
  );
}