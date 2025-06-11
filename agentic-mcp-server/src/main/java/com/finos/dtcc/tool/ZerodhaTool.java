package com.finos.dtcc.tool;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import okhttp3.*;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.time.Duration;

@Slf4j
@Component
public class ZerodhaTool {

    private static final String URL = "http://54.69.201.106:5678/webhook/zerodha-agent-chat";

    @Tool(name = "ZerodhaChat", description = """
            This tool interacts with Zerodha's trading platform to perform various operations related to user accounts, holdings, positions, and orders. 
            It allows users to retrieve profile information, holdings, positions, and order history, as well as place and cancel orders. 
            The tool also supports user authentication via login and request token generation. Following are the available operations:
            get-profile:Retrieves comprehensive user profile information from Zerodha account including user ID, username, email, phone, PAN, segments enabled, and account status
            get-holdings:Fetches all current stock holdings in the user's portfolio including quantity, average price, current market value, P&L, and other holding details
            get-positions:Retrieves all current trading positions (both intraday and overnight) showing quantity, buy/sell prices, realized and unrealized P&L for each position
            get-order-history:Fetches detailed order history and status information for a specific order ID, including all order modifications, execution details, and timestamps
            place-order:Places a buy or sell order for stocks/instruments on Zerodha. Supports multiple order types (MARKET, LIMIT, SL, SL-M), products (CNC, MIS, NRML), variety (amo, regular, co, bo) and exchanges (NSE, BSE). Default settings: exchange='NSE', product='CNC', order_type='MARKET'
            cancel-order:Cancels a pending order using the order ID and variety. Works for open orders that haven't been executed yet. Returns cancellation status and updated order information
            login:Authenticates the user and provides url for login
            login-using-request-token:When user provides the request token, this tool will generate the session. This will be used to login to the server
            """)
    public JsonNode zerodhaChat(String message) throws Exception {
        log.info("Zerodha chat request received: {}", message);

        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(Duration.ofMinutes(2))
                .readTimeout(Duration.ofMinutes(2))
                .writeTimeout(Duration.ofMinutes(2))
                .build();
        ObjectMapper objectMapper = new ObjectMapper();

        MediaType mediaType = MediaType.parse("text/plain");
        RequestBody body = RequestBody.create(message, mediaType);
        Request request = new Request.Builder()
                .url(URL)
                .method("POST", body)
                .addHeader("Content-Type", "text/plain")
                .build();

        log.info("Zerodha chat request sent to URL: {}", URL);
        try (Response execute = client.newCall(request).execute()) {
            if (execute.isSuccessful() && execute.body() != null) {
                String json = execute.body().string();
                log.info("Zerodha chat response: {}", json);
                return objectMapper.readTree(json);
            } else {
                log.error("Failed to process Zerodha chat request: {}", execute.message());
            }
        } catch (Exception e) {
            log.error("Error sending Zerodha chat request: {}", e.getMessage());
        }

        return objectMapper.createObjectNode().put("error", "Failed to process Zerodha chat request");
    }
}
