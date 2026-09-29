import { useState, useCallback, useRef } from 'react'
import { useSession } from './chat/useSession'
import { useMessages } from './chat/useMessages'
import { ChatService } from '../services/chatService'

export const useStreamingChat = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [messageCount, setMessageCount] = useState(0)
  const [messageLimit, setMessageLimit] = useState(8)

  const { sessionId, startNewSession } = useSession()
  const { messages, addMessage, updateLastMessage, resetMessages } = useMessages()
  const shouldStopRef = useRef(false)

  const stopAnswering = useCallback(() => {
    shouldStopRef.current = true
  }, [])

  const sendMessage = async (chatRequest) => {
    setIsLoading(true)
    setError(null)

    try {
      // Keep the previous conversation before adding the new question
      const history = messages.map(({ role, content }) => ({
        role,
        content
      }))

      addMessage({
        role: 'user',
        content: chatRequest.message
      })

      const response = await ChatService.sendMessage(
        chatRequest.message,
        history
      )

      // Update question counter from backend
      setMessageCount(response.message_count)
      setMessageLimit(response.message_limit)

      addMessage({
        role: 'assistant',
        content: response.answer,
        sources: response.sources
      })

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const startNewChat = useCallback(() => {
    const newSessionId = startNewSession()
    resetMessages()
    setMessageCount(0)
    return newSessionId
  }, [startNewSession, resetMessages])

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    sessionId,
    startNewChat,
    stopAnswering,
    messageCount,
    messageLimit
  }
}