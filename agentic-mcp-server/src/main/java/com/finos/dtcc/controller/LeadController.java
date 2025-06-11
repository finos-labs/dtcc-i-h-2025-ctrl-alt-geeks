package com.finos.dtcc.controller;

import com.finos.dtcc.entity.Lead;
import com.finos.dtcc.repository.LeadRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/leads")
public class LeadController {

    private final LeadRepository leadRepository;

    public LeadController(LeadRepository leadRepository) {
        this.leadRepository = leadRepository;
    }

    /**
     * Fetches a lead by its contact number.
     *
     * @param contactNumber the contact number of the lead
     * @return ResponseEntity containing the Lead object if found, or an error message if not found
     */
    @GetMapping("/{contactNumber}")
    public ResponseEntity<Lead> getLead(@PathVariable String contactNumber) {
        log.info("Fetching lead by contact number: {}", contactNumber);
        Lead lead = leadRepository.findFirstByContactNumber(contactNumber)
                .orElseThrow(() -> new IllegalArgumentException("Lead not found with contact: " + contactNumber));
        log.info("Lead status: {}", lead.getStatus());
        return ResponseEntity.ok(lead);
    }

    @GetMapping
    public ResponseEntity<List<Lead>> getAllLeads() {
        log.info("Fetching all leads");
        List<Lead> leads = leadRepository.findAllByStatus("new");
        log.info("Total leads fetched: {}", leads.size());
        return ResponseEntity.ok(leads);
    }

}
