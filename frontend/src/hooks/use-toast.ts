import * as React from "react"

type ToastType = "success" | "error"

interface Toast {
  id: string
  type: ToastType
  title: string
  description?: string
}

const toasts: Toast[] = []
const listeners: Array<(toasts: Toast[]) => void> = []

let toastId = 0

function addToast(toast: Omit<Toast, "id">) {
  const id = (++toastId).toString()
  const newToast = { ...toast, id }
  toasts.push(newToast)
  
  listeners.forEach(listener => listener([...toasts]))
  
  setTimeout(() => {
    removeToast(id)
  }, 3000)
  
  return id
}

function removeToast(id: string) {
  const index = toasts.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.splice(index, 1)
    listeners.forEach(listener => listener([...toasts]))
  }
}

export function useToast() {
  const [toastList, setToastList] = React.useState<Toast[]>([...toasts])
  
  React.useEffect(() => {
    listeners.push(setToastList)
    return () => {
      const index = listeners.indexOf(setToastList)
      if (index > -1) listeners.splice(index, 1)
    }
  }, [])
  
  const toast = React.useCallback((toast: Omit<Toast, "id">) => {
    return addToast(toast)
  }, [])
  
  return { toasts: toastList, toast }
}