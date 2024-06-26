from typing import List, Optional
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from .. database import engine, get_db 
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# POSTS ENDPOINTS


# get all posts


# @router.get("/")
@router.get("/",  response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
   
    # print(posts)

    results = db.query(models.Post, func.count(models.Vote.post_id)).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = []
    for post, votes_count in results:
        post_dict = post.__dict__
        post_dict.update({"votes": votes_count})
        posts.append(post_dict)

    return posts
    

# get  post by id

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # Query the post and count its votes
    post_with_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
                        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
                        .group_by(models.Post.id) \
                        .filter(models.Post.id == id) \
                        .first()

    if not post_with_votes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    post, votes_count = post_with_votes

    # Query the owner of the post
    owner = db.query(models.User).filter(models.User.id == post.owner_id).first()

    # Construct PostOut response model
    post_out = schemas.PostOut(
        published=post.published,
        created_at=post.created_at,
        content=post.content,
        title=post.title,
        id=post.id,
        owner_id=post.owner_id,
        votes=votes_count,
        owner=owner  # Assuming you have a User model linked via owner_id
    )
    
    return post_out

# create post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    # cursor.execute(""" INSERT into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published) )
    # new_post = cursor.fetchone()
    # conn.commit()
    
    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post



# update a post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""  UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING *""" , (post.title, post.content, post.published, (str(id))))
    
    # update_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()


    return post_query.first() 


# delete a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""  DELETE from posts WHERE id = %s RETURNING *""" , (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


