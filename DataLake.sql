-- ===========================
-- TABLE : Societe
-- ===========================

CREATE TABLE Societe (

idSociete SERIAL PRIMARY KEY,
NomSociete VARCHAR(255) NOT NULL,
CodePostalSociete VARCHAR(20),
VilleSociete VARCHAR(100),
RegionSociete VARCHAR(100),
PaysSociete VARCHAR(100)

);

-- ===========================
-- TABLE : Avis
-- ===========================

CREATE TABLE Avis (

idAvis SERIAL PRIMARY KEY,
idSociete INT NOT NULL,
DescriptionAvis TEXT,
AvantageAvis TEXT,
InconvenientAvis TEXT,
NoteMoyenneAvis DECIMAL(2,1),
TitreAvis VARCHAR(255),


CONSTRAINT fk_avis_societe

FOREIGN KEY (idSociete)

REFERENCES Societe(idSociete)


);

-- ===========================
-- TABLE : Emploi
-- ===========================

CREATE TABLE Emploi (

idEmploi SERIAL PRIMARY KEY,
idSociete INT NOT NULL,
libelleEmploi VARCHAR(255) NOT NULL,
descriptifEmploi TEXT,
CodePostalEmploi VARCHAR(20),
VilleEmploi VARCHAR(100),
RegionEmploi VARCHAR(100),
PaysEmploi VARCHAR(100),
CONSTRAINT fk_emploi_societe

FOREIGN KEY (idSociete)

REFERENCES Societe(idSociete)

);

-- ===========================
-- DIMENSION : Emploi
-- ===========================

CREATE TABLE DIM_Emploi (
    idEmploi INT PRIMARY KEY,
    libelleEmploi VARCHAR(255) NOT NULL,
    descriptifEmploi TEXT,
    codePostalEmploi VARCHAR(10),
    villeEmploi VARCHAR(100),
    regionEmploi VARCHAR(100),
    paysEmploi VARCHAR(100) 
);

-- ===========================
-- DIMENSION : Societe
-- ===========================

CREATE TABLE DIM_Societe (
    idSociete INT PRIMARY KEY,
    nomSociete VARCHAR(255) NOT NULL UNIQUE,
    codePostalSociete VARCHAR(10),
    villeSociete VARCHAR(100),
    regionSociete VARCHAR(100),
    paysSociete VARCHAR(100) NOT NULL
);


-- ===========================
-- DIMENSION : Avis
-- ===========================

CREATE TABLE DIM_Avis (
    idAvis INT PRIMARY KEY,
    descriptionAvis TEXT,
    avantageAvis TEXT,
    inconvenientAvis TEXT,
    titreAvis VARCHAR(255)
);

-- ===========================
-- FAIT : Proposition
-- ===========================

CREATE TABLE FACT_Proposition (
    idSociete INT NOT NULL,
    idEmploi INT NOT NULL,
    PRIMARY KEY (idSociete, idEmploi),
    FOREIGN KEY (idSociete) REFERENCES DIM_Societe(idSociete),
    FOREIGN KEY (idEmploi) REFERENCES DIM_Emploi(idEmploi)
);

-- ===========================
-- FAIT : Avis
-- ===========================

CREATE TABLE FACT_Avis (
    idSociete INT NOT NULL,
    idAvis INT NOT NULL,
    noteMoyenneAvis DECIMAL(3, 2),
    nbAvis INT,
    PRIMARY KEY (idSociete, idAvis),
    FOREIGN KEY (idSociete) REFERENCES DIM_Societe(idSociete),
    FOREIGN KEY (idAvis) REFERENCES DIM_Avis(idAvis)
); 


CREATE OR REPLACE PROCEDURE sp_load_dim_societe()
LANGUAGE plpgsql
AS $$
BEGIN

    TRUNCATE TABLE dim_Societe CASCADE;
    INSERT INTO dim_Societe (
        idSociete,
        nomSociete,
        CodePostalSociete,
        VilleSociete,
        RegionSociete,
        PaysSociete
    )

    SELECT
        idSociete,
        NomSociete,
        CodePostalSociete,
        VilleSociete,
        RegionSociete,
        PaysSociete
    FROM Societe;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_load_dim_emploi()
LANGUAGE plpgsql
AS $$
BEGIN

    TRUNCATE TABLE dim_Emploi CASCADE;
    INSERT INTO dim_Emploi (
        idEmploi,
        libelleEmploi,
        descriptifEmploi,
        CodePostalEmploi,
        VilleEmploi,
        RegionEmploi,
        PaysEmploi

    )

    SELECT
        idEmploi,
        libelleEmploi,
        descriptifEmploi,
        CodePostalEmploi,
        VilleEmploi,
        RegionEmploi,
        PaysEmploi
    FROM Emploi;

END;
$$;



CREATE OR REPLACE PROCEDURE sp_load_dim_avis()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE dim_Avis CASCADE; 

    INSERT INTO dim_Avis (
        idAvis,
        DescriptionAvis,
        AvantageAvis,
        InconvenientAvis,
        TitreAvis
    )

    SELECT
        idAvis,
        DescriptionAvis,
        AvantageAvis,
        InconvenientAvis,
        TitreAvis
    FROM Avis;
END;
$$;


CREATE OR REPLACE PROCEDURE sp_load_fact_proposition()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE FACT_Proposition;

    INSERT INTO FACT_Proposition (
        idSociete,
        idEmploi,
        NbEmploi
    )
    SELECT
        e.idSociete,
        e.idEmploi,
        COUNT(*) AS NbEmploi  
    FROM
        Emploi AS e 
    GROUP BY
        e.idSociete,
        e.idEmploi;
END;
$$;



CREATE OR REPLACE PROCEDURE sp_load_fact_avis()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE FACT_Avis;

    INSERT INTO FACT_Avis (
        idSociete,
        idAvis,
        NoteMoyenneAvis,
        NbAvis
    )
    SELECT
        a.idSociete,
        a.idAvis,
        a.NoteMoyenneAvis, 
        1 AS NbAvis          
    FROM
        Avis AS a;  
END;
$$;

