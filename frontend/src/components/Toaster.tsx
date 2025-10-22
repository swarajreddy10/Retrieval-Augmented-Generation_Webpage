import { useToast } from '../hooks/use-toast'

import { cn } from '../lib/utils'

export function Toaster() {
  const { toasts } = useToast()

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            "flex items-start gap-3 p-4 rounded-lg shadow-lg border backdrop-blur-sm animate-in slide-in-from-top-2 min-w-[300px] max-w-[400px]",
            toast.type === "success" 
              ? "bg-background border-green-200 dark:border-green-800" 
              : "bg-background border-red-200 dark:border-red-800"
          )}
        >
          <div className="flex-1">
            <div className="font-medium text-foreground">{toast.title}</div>
            {toast.description && (
              <div className="text-sm text-muted-foreground mt-1">{toast.description}</div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}