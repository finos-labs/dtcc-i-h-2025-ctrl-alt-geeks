package com.finos.dtcc.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.finos.dtcc.entity.Client;

@Repository
public interface ClientRepository extends JpaRepository<Client, String> {

}
