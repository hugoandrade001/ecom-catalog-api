package com.ecom.productcatalog.services;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.repository.CatalogRepository;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class CatalogService {

    private CatalogRepository catalogRepository;

    public CatalogService(CatalogRepository catalogRepository) {
        this.catalogRepository = catalogRepository;
    }

    public List<CatalogModel> findAll() {
        return catalogRepository.findAll();
    }
}
