package com.finos.dtcc.controller;

import com.finos.dtcc.entity.Client;
import com.finos.dtcc.repository.ClientRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@Slf4j
@RestController
@RequestMapping("/clients")
public class ClientController {

    private final ClientRepository clientRepository;

    public ClientController(ClientRepository clientRepository) {
        this.clientRepository = clientRepository;
    }

    @GetMapping
    public ResponseEntity<List<Client>> getClients() {
        log.info("Fetching all clients sorted by last modified date in descending order");
        List<Client> clients = clientRepository.findAll(Sort.by("lastModifiedDate").descending());
        log.info("Number of clients fetched: {}", clients.size());
        return ResponseEntity.ok(clients);
    }

}
