package com.ecom.productcatalog.controllers;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.services.CatalogService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/categories")
public class CatalogController {

    private final CatalogService catalogService;

    public CatalogController(CatalogService catalogService) {
        this.catalogService = catalogService;
    }

    @GetMapping
    public List<CatalogModel> findAllCategories() {
        return catalogService.findAll();
    }
}
