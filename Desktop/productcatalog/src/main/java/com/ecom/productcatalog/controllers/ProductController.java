package com.ecom.productcatalog.controllers;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.models.ProductsModel;
import com.ecom.productcatalog.services.ProductService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public List<ProductsModel> findAllProducts() {
        return productService.findAll();
    }

    @GetMapping("/category/{categoryId}")
    public List<ProductsModel> findByCategoryId(@PathVariable CatalogModel categoryId) {
        return productService.findByCategory(categoryId);
    }
}
