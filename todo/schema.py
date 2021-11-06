instructions = [ 
    """
    CREATE TABLE IF NOT EXISTS user (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS todo(
        id INT AUTO_INCREMENT,
        create_by INT NOT NULL,
        create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL,
        PRIMARY KEY(id),
        foreign key(create_by) REFERENCES user (id)
    );
    """
]

