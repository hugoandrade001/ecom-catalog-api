package com.ecom.productcatalog.seed;

import com.ecom.productcatalog.models.CatalogModel;
import com.ecom.productcatalog.repository.CatalogRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class CatalogSeeder implements CommandLineRunner {

    private final CatalogRepository catalogRepository;

    public CatalogSeeder(CatalogRepository catalogRepository) {
        this.catalogRepository = catalogRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        if (catalogRepository.count() == 0) {
            CatalogModel electronics = new CatalogModel();
            electronics.setName("Eletrônicos");
            electronics.setSize(10.0);

            CatalogModel fashion = new CatalogModel();
            fashion.setName("Moda");
            fashion.setSize(5.5);

            CatalogModel books = new CatalogModel();
            books.setName("Livros");
            books.setSize(3.0);

            catalogRepository.save(electronics);
            catalogRepository.save(fashion);
            catalogRepository.save(books);

            System.out.println("✅ Dados de categoria inseridos no banco.");
        }
    }
}
