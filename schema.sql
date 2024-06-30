create table livros (id serial primary key, 
    nome varchar(255), isbn varchar(255), 
    created_at timestamp default now (), updated_at timestamp default now ());
