from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas.contacts import ContactCreate

async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts

async def get_contact_by_id(contact_id: int, db: Session):
    contacts = db.query(Contact).filter_by(id=contact_id).first()
    return contacts

async def get_contact_by_email(email: str, db: Session):
    contacts = db.query(Contact).filter_by(email=email).first()
    return contacts

async def search_contact(query: str, db: Session):
    contact = db.query(Contact).filter(Contact.firstname.ilike(f'%{query}%')).all()
    if contact:
        return contact
    contact = db.query(Contact).filter(Contact.lastname.ilike(f'%{query}%')).all()
    if contact:
        return contact
    contact = db.query(Contact).filter(Contact.email.ilike(f'%{query}%')).all()
    if contact:
        return contact

async def create_contact(body: ContactCreate, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactCreate, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact

async def delete_contact(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_birthday_per_week(db: Session):
    contacts = []
    all_contacts = db.query(Contact).all()
    for contact in all_contacts:
        if timedelta(0) <= (datetime.now() - (contact.birthday.replace(year=int((datetime.now()).year)))) <= timedelta(7):
            contacts.append(contact)
    return contacts