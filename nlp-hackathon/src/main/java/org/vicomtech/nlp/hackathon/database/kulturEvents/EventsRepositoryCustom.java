package org.vicomtech.nlp.hackathon.database.kulturEvents;

import java.util.List;

import org.vicomtech.nlp.hackathon.model.KulturalEvent;

public interface EventsRepositoryCustom {

	public List<KulturalEvent>findByCriteria(String municipality,String eventType,String desiredDate);
	
}
