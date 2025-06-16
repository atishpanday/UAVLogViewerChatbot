<template>
    <div>
        <button class="toggle-button" @click="toggleChat">
            <span v-if="!isOpen">Ask AI</span>
            <span v-else>Close</span>
        </button>
        <div v-if="isOpen" class="chatbot">
            <div class="chatbot-header">
                <h3>AI Assistant</h3>
            </div>
            <div class="chatbot-messages" ref="messageContainer">
                <div v-if="!state.file" class="database-message">
                    <p>No flight logs uploaded yet</p>
                </div>
                <div v-else-if="state.databaseCreated" class="database-message">
                    <p>Agent is ready to help you with your flight logs</p>
                </div>
                <div v-else class="database-message processing">
                    <p>Processing your flight logs...</p>
                </div>
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
                    <div v-if="message.role === 'user'">{{ message.content }}</div>
                    <div v-else v-html="renderMarkdown(message.content)"></div>
                </div>
                <div v-if="loading" class="message assistant thinking">
                    <span v-if="!analyzing">Thinking...</span>
                    <span v-else>Analyzing flight logs...</span>
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" v-model="newMessage" @keyup.enter="sendMessage"
                placeholder="Type a message..." :disabled="loading">
                <button @click="sendMessage" :disabled="loading">Send</button>
            </div>
        </div>
    </div>
</template>

<script>
import { marked } from 'marked'
import { store } from './Globals'

export default {
    name: 'Chatbot',
    data () {
        return {
            messages: [],
            newMessage: '',
            isOpen: false,
            loading: false,
            analyzing: false,
            state: store
        }
    },
    methods: {
        async sendMessage () {
            if (this.newMessage.trim()) {
                // Add user message
                this.messages.push({
                    role: 'user',
                    content: this.newMessage
                })
                this.newMessage = ''
                this.loading = true

                // Set analyzing to true after 5 seconds
                setTimeout(() => {
                    this.analyzing = true
                }, 5000)

                try {
                    const response = await fetch('http://localhost:8000/chatbot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            messages: this.messages
                        })
                    })

                    if (!response.ok) {
                        throw new Error('Network response was not ok')
                    }
                    const decoder = new TextDecoder()

                    const reader = response.body.getReader()
                    while (true) {
                        const { value, done } = await reader.read()
                        if (done) break
                        const chunk = decoder.decode(value, { stream: true })
                        if (this.messages[this.messages.length - 1].role === 'user') {
                            this.loading = false
                            this.analyzing = false
                            this.messages.push({
                                role: 'assistant',
                                content: chunk
                            })
                        } else {
                            this.messages[this.messages.length - 1].content += chunk
                        }
                    }
                } catch (error) {
                    this.loading = false
                    this.analyzing = false
                    console.error('Error:', error)
                    this.messages.push({
                        role: 'assistant',
                        content: 'Sorry, there was an error processing your message.'
                    })
                } finally {
                    this.$nextTick(() => {
                        this.scrollToBottom()
                    })
                }
            }
        },
        scrollToBottom () {
            const container = this.$refs.messageContainer
            if (container) {
                // Use setTimeout to ensure DOM has updated
                setTimeout(() => {
                    container.scrollTo({
                        top: container.scrollHeight,
                        behavior: 'smooth'
                    })
                }, 0)
            }
        },
        toggleChat () {
            this.isOpen = !this.isOpen
        },
        renderMarkdown (content) {
            return marked(content)
        }
    },
    watch: {
        messages () {
            this.$nextTick(() => {
                this.scrollToBottom()
            })
        }
    }
}
</script>

<style scoped>
p {
    margin: 0;
    padding: 0;
}
.toggle-button {
    position: fixed;
    bottom: 10px;
    right: 10px;
    padding: 8px 15px;
    background: #004080;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    z-index: 1000;
}

.toggle-button:hover {
    background: #0056b3;
}

.chatbot {
    width: 400px;
    height: 600px;
    background: #333333;
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    z-index: 1000;
    position: fixed;
    bottom: 60px;
    right: 10px;
}

.chatbot-header {
    padding: 10px;
    background: #004080;
    color: white;
    border-radius: 4px 4px 0 0;
}

.chatbot-header h3 {
    margin: 0;
    font-size: 16px;
}

.database-message {
    width: 60%;
    margin: 2px auto;
    padding: 10px;
    background: #4d4d4d;
    color: white;
    border: 1px solid #fff;
    border-radius: 4px;
    border-radius: 4px;
    text-align: center;
}

.chatbot-messages {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
}

.message {
    margin: 4px 0;
    max-width: 100%;
    word-wrap: break-word;
}

.user {
    padding: 8px 12px;
    border-radius: 4px;
    background-color: rgba(0, 64, 128, 0.5);
    border: 2px solid #004080;
    color: white;
}

.assistant {
    padding: 8px 4px;
    color: white;
}

.thinking {
    font-style: italic;
    opacity: 0.7;
}

.chatbot-input {
    padding: 10px;
    border-top: 1px solid #ddd;
    display: flex;
}

.chatbot-input input {
    flex: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 5px;
    background: #333333;
    color: white;
}

.chatbot-input input:disabled,
.chatbot-input button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.chatbot-input button {
    padding: 8px 15px;
    background: #004080;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.chatbot-input button:hover:not(:disabled) {
    background: #0056b3;
}
</style>
