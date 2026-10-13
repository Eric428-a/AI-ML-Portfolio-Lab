import {
    type ReactNode,
    useEffect,
    useId,
  } from "react";
  import { createPortal } from "react-dom";
  import { X } from "lucide-react";
  
  interface ModalProps {
    open: boolean;
    title: string;
    description?: string;
    children: ReactNode;
    onClose: () => void;
    width?: string;
  }
  
  export default function Modal({
    open,
    title,
    description,
    children,
    onClose,
    width = "480px",
  }: ModalProps) {
    const titleId = useId();
  
    useEffect(() => {
      if (!open) return;
  
      const onKeyDown = (event: KeyboardEvent) => {
        if (event.key === "Escape") onClose();
      };
  
      window.addEventListener("keydown", onKeyDown);
  
      const previousOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
  
      return () => {
        window.removeEventListener("keydown", onKeyDown);
        document.body.style.overflow = previousOverflow;
      };
    }, [open, onClose]);
  
    if (!open) return null;
  
    return createPortal(
      <div
        className="modal-backdrop"
        onMouseDown={(event) => {
          if (event.target === event.currentTarget) {
            onClose();
          }
        }}
      >
        <section
          className="modal-panel"
          style={{ maxWidth: width }}
          role="dialog"
          aria-modal="true"
          aria-labelledby={titleId}
        >
          <header className="modal-header">
            <div>
              <h2 id={titleId}>{title}</h2>
              {description && <p>{description}</p>}
            </div>
  
            <button
              type="button"
              className="icon-button"
              onClick={onClose}
              aria-label="Close dialog"
            >
              <X size={18} />
            </button>
          </header>
  
          <div className="modal-content">{children}</div>
        </section>
      </div>,
      document.body,
    );
  }