from typing import List
from datetime import date

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts')


@router.get("/", description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def list_contacts(skip: int = 0, limit: int = 30, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
            Retrieves a list of contacts for a specific user with specified pagination parameters.

            :param skip: The number of contacts to skip.
            :type skip: int
            :param limit: The maximum number of contacts to return.
            :type limit: int
            :param current_user: The user to retrieve contacts for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: A list of contacts.
            :rtype: List[Contact]
            """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/find")
async def find(first_name: str | None = None, last_name: str | None = None, email: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
            Retrieves a list of contacts for a specific user that matches the specified parameters.

            :param first_name: First name of the contact to retrieve.
            :type first_name: str
            :param last_name: Last name of the contact to retrieve.
            :type last_name: str
            :param email: Email of the contact to retrieve.
            :type email: str
            :param current_user: The user to retrieve contacts for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: A list of contacts or Exception.
            :rtype: List[Contact]
            """
    contacts = await repository_contacts.find_contacts(first_name, last_name, email, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.get("/congratulate")
async def birthdays_per_week(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
            Retrieves a list of contacts for a specific user that will celebrate birthday in next 7 days.

            :param current_user: The user to retrieve contacts for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: A list of contacts.
            :rtype: List[Contact]
            """
    contacts = await repository_contacts.congratulate(current_user, db)
    return contacts


@router.get("/{contact_id}")
async def contact_info(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
            Retrieves a single contact with the specified ID for a specific user.

            :param contact_id: The ID of the contact to retrieve.
            :type contact_id: int
            :param current_user: The user to retrieve the contact for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: The contact with the specified ID, or Exception if it does not exist.
            :rtype: Contact
            """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
            Creates a new contact for a specific user.

            :param body: The data for the contact to create.
            :type body: ContactModel
            :param current_user: The user to create the contact for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: The newly created contact.
            :rtype: Contact
            """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
            Updates a single contact with the specified ID for a specific user.

            :param contact_id: The ID of the note to update.
            :type contact_id: int
            :param body: The updated data for the contact.
            :type body: ContactModel
            :param current_user: The user to update the contact for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: The updated contact, or Exception if it does not exist.
            :rtype: Contact
            """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
            Removes a single contact with the specified ID for a specific user.

            :param contact_id: The ID of the contact to remove.
            :type contact_id: int
            :param current_user: The user to remove the contact for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: The removed contact, or Exception if it does not exist.
            :rtype: Contact
            """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact




