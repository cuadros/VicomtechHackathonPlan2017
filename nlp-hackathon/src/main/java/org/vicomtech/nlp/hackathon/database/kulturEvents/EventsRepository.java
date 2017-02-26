package org.vicomtech.nlp.hackathon.database.kulturEvents;

import java.util.Date;
import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import org.vicomtech.nlp.hackathon.model.KulturalEvent;

@Repository
public interface EventsRepository extends EventsRepositoryCustom, MongoRepository<KulturalEvent,String>{

	List<KulturalEvent> findByMunicipalityIgnoreCase(String municipality);
	
	List<KulturalEvent> findByEventTypeIgnoreCase(String eventType);
	
	List<KulturalEvent> findByMunicipalityIgnoreCaseAndEventTypeIgnoreCase(String municipality,String eventType);
	
	List<KulturalEvent> findByStartDateBeforeAndEndDateAfter(Date desiredDate,Date desiredDate2);
	
}
