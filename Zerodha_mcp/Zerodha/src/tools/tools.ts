import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { KiteController } from "../app/KiteController";

console.log("TOOLS");
const kiteController = new KiteController();

// Create an MCP server
const server = new McpServer({
  name: "Demo",
  version: "1.0.0"
});

server.tool("get-profile", "Retrieves comprehensive user profile information from Zerodha account including user ID, username, email, phone, PAN, segments enabled, and account status", {}, async (params) => {
    const profile = await kiteController.getProfile();
    return {
      content: [{ type: "text", text: JSON.stringify(profile, null, 2) }]
    };
  });

server.tool("get-holdings", "Fetches all current stock holdings in the user's portfolio including quantity, average price, current market value, P&L, and other holding details", {}, async (params) => {
  const holdings = await kiteController.getHoldings();
    return {
      content: [{ type: "text", text: JSON.stringify(holdings, null, 2) }]
    };
});

server.tool("get-positions", "Retrieves all current trading positions (both intraday and overnight) showing quantity, buy/sell prices, realized and unrealized P&L for each position", {}, async (params) => {
  const holdings = await kiteController.getPositions();
    return {
      content: [{ type: "text", text: JSON.stringify(holdings, null, 2) }]
    };
});

server.tool("get-order-history", "Fetches detailed order history and status information for a specific order ID, including all order modifications, execution details, and timestamps", { order_id: z.string()  }, async (params) => {
  const holdings = await kiteController.getOrderHistory(params.order_id);
    return {
      content: [{ type: "text", text: JSON.stringify(holdings, null, 2) }]
    };
});


server.tool("place-order", "Places a buy or sell order for stocks/instruments on Zerodha. Supports multiple order types (MARKET, LIMIT, SL, SL-M), products (CNC, MIS, NRML), variety (amo, regular, co, bo) and exchanges (NSE, BSE). Default settings: exchange='NSE', product='CNC', order_type='MARKET'", 
  { 
    stock: z.string(), 
    quantity: z.number(), 
    transactionType: z.enum(['BUY', 'SELL']),
    variety: z.string().optional().default("amo"),
    exchange: z.string().optional().default("NSE"),
    product: z.string().optional().default("CNC"),
    order_type: z.string().optional().default("MARKET")
  },
  async (params) => {
  const holdings = await kiteController.placeOrder(
    params.stock, 
    params.quantity, 
    params.transactionType,
    params.variety,
    params.exchange,
    params.product,
    params.order_type
  ); 
  return {
    content: [{ type: "text", text: JSON.stringify(holdings, null, 2) }]
  };
});

server.tool("cancel-order", "Cancels a pending order using the order ID and variety. Works for open orders that haven't been executed yet. Returns cancellation status and updated order information", 
  { 
    order_id: z.string(), 
    variety: z.string().optional().default("amo") 
  }, 
  async (params) => {
  const holdings = await kiteController.cancelOrder(params.order_id, params.variety);
    return {
      content: [{ type: "text", text: JSON.stringify(holdings, null, 2) }]
    };
});

server.tool("login", "Authenticates the user and provides url for login",
  {},
  async (params) => {
    const url = await kiteController.kc.getLoginURL();
    return {
      content: [{ type: "text", text: JSON.stringify(url, null, 2) }]
    };
  }
)

server.tool("login-using-request-token", "When user provides the request token, this tool will generate the session. This will be used to login to the server",
  {
    request_token: z.string(),
  },
  async (params) => {
    const token_response = await kiteController.generateSession(params.request_token);
    return {
      content: [{ type: "text", text: JSON.stringify(token_response, null, 2) }]
    };
  }
)

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
(async () => {
  await server.connect(transport);
})();