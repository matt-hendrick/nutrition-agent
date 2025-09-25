const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

interface ChatRequest {
  user_input: string
  thread_id: string
}

interface ChatResponse {
  response: string
}

export async function sendMessage(userInput: string, threadId: string): Promise<string> {
  try {
    const requestBody: ChatRequest = {
      user_input: userInput,
      thread_id: threadId,
    }

    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data: ChatResponse = await response.json()
    return data.response
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}