from typing import List
from datetime import date, datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
        Retrieves a list of contacts for a specific user with specified pagination parameters.

        :param skip: The number of contacts to skip.
        :type skip: int
        :param limit: The maximum number of contacts to return.
        :type limit: int
        :param user: The user to retrieve contacts for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: A list of contacts.
        :rtype: List[Contact]
        """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
        Retrieves a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to retrieve.
        :type contact_id: int
        :param user: The user to retrieve the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The contact with the specified ID, or None if it does not exist.
        :rtype: Contact | None
        """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
        Creates a new contact for a specific user.

        :param body: The data for the contact to create.
        :type body: ContactModel
        :param user: The user to create the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The newly created contact.
        :rtype: Contact
        """
    if body.birthday:
        body.birthday = datetime.strptime(body.birthday, '%d-%m-%Y').date()
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone=body.phone, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
        Updates a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to update.
        :type contact_id: int
        :param body: The updated data for the contact.
        :type body: ContactModel
        :param user: The user to update the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The updated contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = datetime.strptime(body.birthday, '%d-%m-%Y').date()
        contact.user_id = user.id
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
        Removes a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to remove.
        :type contact_id: int
        :param user: The user to remove the contact for.
        :type user: User
        :param db: The database session.
        :type db: Session
        :return: The removed contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def find_contacts(first_name, last_name, email, user: User, db: Session) -> List[Contact] | None:
    """
            Retrieves a list of contacts for a specific user that matches the specified parameters.

            :param first_name: First name of the contact to retrieve.
            :type first_name: str
            :param last_name: Last name of the contact to retrieve.
            :type last_name: str
            :param email: Email of the contact to retrieve.
            :type email: str
            :param user: The user to retrieve contacts for.
            :type user: User
            :param db: The database session.
            :type db: Session
            :return: A list of contacts.
            :rtype: List[Contact]
            """
    if first_name:
        return db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == user.id)).all()
    if last_name:
        return db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == user.id)).all()
    if email:
        return db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).all()
    return None


async def congratulate(user: User, db: Session):
    """
            Retrieves a list of contacts for a specific user that will celebrate birthday in next 7 days.

            :param user: The user to retrieve contacts for.
            :type user: User
            :param db: The database session.
            :type db: Session
            :return: A list of contacts.
            :rtype: List[Contact]
            """
    current = date.today()
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    result = []
    for contact in contacts:
        if contact.birthday:
            bd_this_year = date(day=contact.birthday.day, month=contact.birthday.month, year=current.year)
            delta = bd_this_year - current
            if delta.days in range(0, 8):
                result.append(contact)
    return result

