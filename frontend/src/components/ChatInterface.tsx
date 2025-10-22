import { useState, useRef, useEffect } from 'react'
import { queryDocuments, uploadFiles } from '../services/api'
import { Message } from '../types'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Avatar, AvatarFallback } from './ui/avatar'
import { Send, Paperclip, Sparkles, User, Bot, FileText, Brain, Zap, Search, Upload, Database, Cpu, Globe, Lock, Star, Lightbulb, Target, Rocket } from 'lucide-react'
import { cn } from '../lib/utils'
import { useToast } from '../hooks/use-toast'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedFileNames, setUploadedFileNames] = useState<string[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      isUser: true,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await queryDocuments(input, false)
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.answer,
        isUser: false,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Query failed:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error processing your question.',
        isUser: false,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (files: FileList) => {
    if (!files.length) return
    
    setUploading(true)
    try {
      await uploadFiles(files)
      const fileNames = Array.from(files).map(f => f.name)
      
      setUploadedFileNames(prev => [...prev, ...fileNames])
      
      toast({
        type: "success",
        title: `✅ ${files.length} file${files.length > 1 ? 's' : ''} uploaded successfully`,
        description: fileNames.join(', ')
      })
    } catch (error) {
      console.error('Upload failed:', error)
      toast({
        type: "error",
        title: "❌ Upload failed",
        description: "Please try again or check file format"
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-background via-background to-muted/20">
      {/* Header */}
      <div className="flex items-center justify-center p-4 border-b border-border/50 bg-background/80 backdrop-blur-xl">
        <h1 className="text-lg font-semibold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
          Echo AI
        </h1>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="relative flex items-center justify-center h-full overflow-hidden">
            {/* Floating Icons */}
            <div className="absolute inset-0 pointer-events-none">
              {/* Top row */}
              <FileText className="absolute top-16 left-16 h-7 w-7 text-blue-500/15 animate-float-fade" style={{animationDelay: '0s'}} />
              <Brain className="absolute top-20 left-1/3 h-8 w-8 text-purple-500/15 animate-float-fade" style={{animationDelay: '2s'}} />
              <Search className="absolute top-16 right-1/3 h-7 w-7 text-green-500/15 animate-float-fade" style={{animationDelay: '4s'}} />
              <Zap className="absolute top-20 right-16 h-6 w-6 text-yellow-500/15 animate-float-fade" style={{animationDelay: '6s'}} />
              
              {/* Middle-top row */}
              <Upload className="absolute top-1/3 left-20 h-8 w-8 text-indigo-500/15 animate-float-fade" style={{animationDelay: '1s'}} />
              <Database className="absolute top-1/3 right-20 h-7 w-7 text-slate-500/15 animate-float-fade" style={{animationDelay: '3s'}} />
              
              {/* Center */}
              <Bot className="absolute top-1/2 left-1/4 h-9 w-9 text-emerald-500/15 animate-float-fade" style={{animationDelay: '5s'}} />
              <Cpu className="absolute top-1/2 right-1/4 h-8 w-8 text-orange-500/15 animate-float-fade" style={{animationDelay: '7s'}} />
              
              {/* Middle-bottom row */}
              <Globe className="absolute bottom-1/3 left-20 h-6 w-6 text-teal-500/15 animate-float-fade" style={{animationDelay: '1.5s'}} />
              <Lock className="absolute bottom-1/3 right-20 h-7 w-7 text-red-500/15 animate-float-fade" style={{animationDelay: '3.5s'}} />
              
              {/* Bottom row */}
              <Star className="absolute bottom-16 left-16 h-6 w-6 text-amber-500/15 animate-float-fade" style={{animationDelay: '2.5s'}} />
              <Lightbulb className="absolute bottom-20 left-1/3 h-8 w-8 text-lime-500/15 animate-float-fade" style={{animationDelay: '4.5s'}} />
              <Target className="absolute bottom-16 right-1/3 h-6 w-6 text-rose-500/15 animate-float-fade" style={{animationDelay: '6.5s'}} />
              <Rocket className="absolute bottom-20 right-16 h-7 w-7 text-violet-500/15 animate-float-fade" style={{animationDelay: '0.5s'}} />
            </div>
            
            <div className="text-center max-w-md mx-auto p-8 relative z-10">
              <div className="mb-6">
                <div className="relative">
                  <Sparkles className="h-16 w-16 mx-auto mb-4 text-primary/70" />
                  <div className="absolute inset-0 h-16 w-16 mx-auto bg-primary/10 rounded-full animate-pulse" />
                </div>
              </div>
              <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
                Hello! I'm Echo AI
              </h2>
              <p className="text-muted-foreground mb-6 leading-relaxed">
                I can help you analyze documents and answer questions about them. 
                Upload files using the 📎 button below and start asking questions!
              </p>
              <div className="grid grid-cols-1 gap-3 text-sm">
                <div className="p-3 rounded-lg bg-muted/30 border border-border/50 backdrop-blur-sm">
                  💡 Ask questions about your documents
                </div>
                <div className="p-3 rounded-lg bg-muted/30 border border-border/50 backdrop-blur-sm">
                  📄 Supports PDF, TXT, and DOCX files
                </div>
                <div className="p-3 rounded-lg bg-muted/30 border border-border/50 backdrop-blur-sm">
                  🔍 Get intelligent, context-aware answers
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  "group w-full text-token-text-primary border-b border-border",
                  message.isUser ? "bg-background" : "bg-muted/30"
                )}
              >
                <div className="flex p-4 gap-4 text-base md:gap-6 md:max-w-2xl lg:max-w-[38rem] xl:max-w-3xl md:py-6 lg:px-0 m-auto">
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className={cn(
                      "text-white font-medium",
                      message.isUser ? "bg-gradient-to-br from-blue-500 to-blue-600" : "bg-gradient-to-br from-green-500 to-emerald-600"
                    )}>
                      {message.isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <div className="prose prose-sm dark:prose-invert max-w-none break-words">
                      <div 
                        className="whitespace-pre-wrap"
                        dangerouslySetInnerHTML={{
                          __html: message.text
                            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            .replace(/\*(.*?)\*/g, '<em>$1</em>')
                            .replace(/^### (.*$)/gm, '<h3 class="text-lg font-semibold mt-4 mb-2">$1</h3>')
                            .replace(/^## (.*$)/gm, '<h2 class="text-xl font-semibold mt-4 mb-2">$1</h2>')
                            .replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mt-4 mb-2">$1</h1>')
                            .replace(/^\* (.*$)/gm, '<li class="ml-4">• $1</li>')
                            .replace(/\n\n/g, '</p><p class="mb-2">')
                            .replace(/^(.)/gm, '<p class="mb-2">$1')
                            .replace(/<p class="mb-2">(<h[1-6]|<li)/g, '$1')
                            .replace(/(<\/h[1-6]>|<\/li>)<\/p>/g, '$1')
                        }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="group w-full text-token-text-primary bg-muted/30 border-b border-border">
                <div className="flex p-4 gap-4 text-base md:gap-6 md:max-w-2xl lg:max-w-[38rem] xl:max-w-3xl md:py-6 lg:px-0 m-auto">
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-gradient-to-br from-green-500 to-emerald-600 text-white">
                      <Bot className="h-4 w-4 animate-pulse" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce delay-100" />
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce delay-200" />
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-border/50 bg-background/80 backdrop-blur-xl">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="flex flex-col gap-3 p-4">
            {uploadedFileNames.length > 0 && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span>Files: {uploadedFileNames.slice(-3).join(', ')}</span>
                {uploadedFileNames.length > 3 && (
                  <span className="text-xs">+{uploadedFileNames.length - 3} more</span>
                )}
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="h-6 px-2 text-xs"
                  onClick={() => setUploadedFileNames([])}
                >
                  Clear
                </Button>
              </div>
            )}
            <div className="flex items-end gap-2">
              <div className="relative flex-1">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={uploading ? "Processing files..." : "Message Echo AI..."}
                  className="pr-12 min-h-[44px] resize-none border-input bg-background/50 backdrop-blur-sm"
                  disabled={loading || uploading}
                />
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".pdf,.txt,.docx"
                  onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
                  className="hidden"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 hover:bg-muted/50"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploading}
                >
                  {uploading ? (
                    <div className="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full" />
                  ) : (
                    <Paperclip className="h-4 w-4" />
                  )}
                </Button>
              </div>
              <Button
                type="submit"
                disabled={loading || uploading || !input.trim()}
                size="icon"
                className="h-11 w-11 bg-primary/90 hover:bg-primary"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}