package com.finos.dtcc.tool;

import com.finos.dtcc.entity.Client;
import com.finos.dtcc.entity.KycDetails;
import com.finos.dtcc.entity.Lead;
import com.finos.dtcc.enums.KycStatus;
import com.finos.dtcc.enums.OnboardingStatus;
import com.finos.dtcc.model.response.OnboardingResponse;
import com.finos.dtcc.repository.ClientRepository;
import com.finos.dtcc.repository.LeadRepository;
import com.finos.dtcc.service.OcrService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;

@Slf4j
@Component
public class ClientTool {

    private final OcrService ocrService;

    private final ClientRepository clientRepository;

    private final LeadRepository leadRepository;

    public ClientTool(OcrService ocrService, ClientRepository clientRepository, LeadRepository leadRepository) {
        this.ocrService = ocrService;
        this.clientRepository = clientRepository;
        this.leadRepository = leadRepository;
    }

    /**
     * This method handles the onboarding process for a user.
     * It processes the images provided in the onboarding request using the OCR
     * service.
     *
     * @param clientId The ID of the client to be onboarded.
     * @return An OnboardingResponse indicating the status of the onboarding
     * process.
     */
    @Tool(name = "ClientOnboarding", description = "Handles client onboarding by processing KYC documents using OCR service.")
    public OnboardingResponse onboard(String clientId) {
        log.info("Onboarding user with ID: {}", clientId);
        // Process the images using OCR service
        var optionalKycDetails = ocrService.process(clientId);

        boolean isKycSuccess = optionalKycDetails.isPresent();
        OnboardingStatus status = isKycSuccess ? OnboardingStatus.SUCCESS : OnboardingStatus.FAILED;
        String message = isKycSuccess ? "Onboarding successful." : "Onboarding failed, please try again later.";
        log.info("Onboarding status for client {}: {}", clientId, status);

        saveClient(clientId, optionalKycDetails);
        updateLeadOnboardingStatus(clientId, isKycSuccess);
        return new OnboardingResponse(clientId, status, message);
    }

    private void saveClient(String clientId, Optional<KycDetails> optionalKycDetails) {
        KycStatus kycStatus = optionalKycDetails.isPresent() ? KycStatus.COMPLETED : KycStatus.FAILED;
        Client client = Client.builder()
                .id(clientId)
                .kycDetails(optionalKycDetails.map(List::of).orElseGet(List::of))
                .kycStatus(kycStatus)
                .build();
        clientRepository.save(client);
    }

    private void updateLeadOnboardingStatus(String clientId, boolean isKycSuccess) {
        Optional<Lead> optionalLead = leadRepository.findFirstByContactNumber(clientId);
        if (optionalLead.isPresent()) {
            Lead lead = optionalLead.get();
            lead.setStatus(isKycSuccess ? "onboarded" : "failed");
            leadRepository.save(lead);
            log.info("Updated lead status for client {}: {}", clientId, lead.getStatus());
        } else {
            log.warn("No lead found for client ID: {}", clientId);
        }
    }

    /**
     * This method retrieves client details by client ID.
     *
     * @param clientId The ID of the client to retrieve.
     * @return The Client object containing the client's details.
     */
    @Tool(name = "GetClient", description = "Retrieves client details by client ID.")
    public Client getClient(String clientId) {
        log.info("Retrieving client with ID: {}", clientId);
        return clientRepository.findById(clientId)
                .orElseThrow(() -> new IllegalArgumentException("Client not found with ID: " + clientId));
    }
}