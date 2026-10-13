import {
    forwardRef,
    type ButtonHTMLAttributes,
    type ReactNode,
  } from "react";
  import { LoaderCircle } from "lucide-react";
  
  type ButtonVariant =
    | "primary"
    | "secondary"
    | "ghost"
    | "danger"
    | "outline";
  
  interface ButtonProps
    extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    loading?: boolean;
    icon?: ReactNode;
    children: ReactNode;
    fullWidth?: boolean;
  }
  
  const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    (
      {
        variant = "primary",
        loading = false,
        icon,
        children,
        fullWidth = false,
        className = "",
        disabled,
        type = "button",
        ...props
      },
      ref,
    ) => {
      return (
        <button
          ref={ref}
          type={type}
          disabled={disabled || loading}
          className={[
            "button",
            `button-${variant}`,
            fullWidth ? "button-full" : "",
            className,
          ]
            .filter(Boolean)
            .join(" ")}
          {...props}
        >
          {loading ? (
            <LoaderCircle className="spin" size={16} />
          ) : (
            icon
          )}
          <span>{children}</span>
        </button>
      );
    },
  );
  
  Button.displayName = "Button";
  
  export default Button;