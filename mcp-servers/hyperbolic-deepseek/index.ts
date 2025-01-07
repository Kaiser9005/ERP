#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ErrorCode, ListToolsRequestSchema, McpError } from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';

const API_URL = 'https://api.hyperbolic.xyz/v1/chat/completions';
const API_KEY = process.env.HYPERBOLIC_API_KEY;
const MODEL_NAME = 'deepseek-ai/DeepSeek-V3';

if (!API_KEY) {
  throw new Error('HYPERBOLIC_API_KEY environment variable is required');
}

class HyperbolicDeepSeekServer {
  private server: Server;
  private axiosInstance;

  constructor() {
    this.server = new Server(
      {
        name: 'hyperbolic-deepseek',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.axiosInstance = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
      },
    });

    this.setupToolHandlers();

    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'chat',
          description: 'Send a message to the DeepSeek model via Hyperbolic',
          inputSchema: {
            type: 'object',
            properties: {
              message: {
                type: 'string',
                description: 'The message to send to the model',
              },
              max_tokens: {
                type: 'number',
                description: 'The maximum number of tokens to generate in the chat completion.',
              },
            },
            required: ['message'],
          },
        },
      ],
    }))

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name !== 'chat') {
        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${request.params.name}`);
      }

      const { message, max_tokens } = request.params.arguments as { message: string; max_tokens?: number };

      try {
        const response = await this.axiosInstance.post('', {
          model: MODEL_NAME,
          messages: [{ role: 'user', content: message }],
          max_tokens: max_tokens || 58197,
          temperature: 0.1,
          top_p: 0.9,
          stream: false,
        });

        return {
          content: [
            {
              type: 'text',
              text: response.data.choices[0].message.content,
            },
          ],
        };
      } catch (error: any) {
        console.error('Error calling Hyperbolic API:', error);
        return {
          content: [{ type: 'text', text: `Error calling Hyperbolic API: ${error.message}` }],
          isError: true,
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Hyperbolic DeepSeek MCP server running on stdio');
  }
}

const server = new HyperbolicDeepSeekServer();
server.run().catch(console.error);
