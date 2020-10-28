select artistToEvent.id, Artist.name, Event.name from Artist
join artistToEvent ON Artist.ID = artistToEvent.artistID
join Event ON artistToEvent.eventID = Event.id



select artistToEvent.id, Artist.name, Event.name, Venue.name from Venue
join Event ON Venue.id = Event.venueID
join artistToEvent on Event.id = artistToEvent.eventID
join Artist ON artistToEvent.artistID = Artist.id
where Venue.name = "Emerson Suites"