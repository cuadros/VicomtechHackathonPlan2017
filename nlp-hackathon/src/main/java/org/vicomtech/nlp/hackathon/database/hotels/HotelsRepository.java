package org.vicomtech.nlp.hackathon.database.hotels;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.vicomtech.nlp.hackathon.model.Hotel;

public interface HotelsRepository extends HotelsRepositoryCustom, MongoRepository<Hotel, String>{

}
