-- ===========================
-- TABLE : Societe
-- ===========================

CREATE TABLE Societe (

idSociete SERIAL PRIMARY KEY,
NomSociete VARCHAR(255) NOT NULL,
CodePostalSociete VARCHAR(20),
VilleSociete VARCHAR(100),
RegionSociete VARCHAR(100),
PaysSociete VARCHAR(100),
MinEffectif INT,
MaxEffectif INT
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
DateAvis DATE,
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
DatePublication DATE,

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
    paysSociete VARCHAR(100) NOT NULL,
    MinEffectif INT, 
    MaxEffectif INT 
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
-- DIMENSION : Temps
-- ===========================

CREATE TABLE DIM_Temps (
    id_temps SERIAL PRIMARY KEY,
    date DATE not null UNIQUE,
    annee INT ,
    mois INT ,
    jours INT
);


-- ===========================
-- FAIT : Proposition
-- ===========================

CREATE TABLE FACT_Proposition (
    idSociete INT NOT NULL,
    idEmploi INT NOT NULL,
    id_temps INT NOT NULL,
    NbEmploi INT,
    PRIMARY KEY (idSociete, idEmploi),
    FOREIGN KEY (idSociete) REFERENCES DIM_Societe(idSociete),
    FOREIGN KEY (idEmploi) REFERENCES DIM_Emploi(idEmploi),
    FOREIGN KEY (id_temps) REFERENCES DIM_Temps(id_temps)
);

-- ===========================
-- FAIT : Avis
-- ===========================

CREATE TABLE FACT_Avis (
    idSociete INT NOT NULL,
    idAvis INT NOT NULL,
    id_temps INT NOT NULL,
    noteMoyenneAvis DECIMAL(3, 2),
    nbAvis INT,
    PRIMARY KEY (idSociete, idAvis),
    FOREIGN KEY (idSociete) REFERENCES DIM_Societe(idSociete),
    FOREIGN KEY (idAvis) REFERENCES DIM_Avis(idAvis),
    FOREIGN KEY (id_temps) REFERENCES DIM_Temps(id_temps)
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
        PaysSociete,
        MinEffectif,
        MaxEffectif
    )

    SELECT
        idSociete,
        NomSociete,
        CodePostalSociete,
        VilleSociete,
        RegionSociete,
        PaysSociete,
        MinEffectif,
        MaxEffectif
    FROM Societe;
END;
$$;

call sp_load_dim_societe();
--select * from dim_societe

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

call sp_load_dim_emploi();
--select * from dim_emploi



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

call sp_load_dim_avis();
--select * from dim_avis


CREATE OR REPLACE PROCEDURE sp_load_dim_temps()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE DIM_Temps RESTART IDENTITY CASCADE; 

    INSERT INTO DIM_Temps (date, annee, mois, jours)
    SELECT DISTINCT
        dt.jour_date AS date,
        EXTRACT(YEAR FROM dt.jour_date) AS annee,
        EXTRACT(MONTH FROM dt.jour_date) AS mois,
        EXTRACT(DAY FROM dt.jour_date) AS jours
    FROM (
        SELECT DatePublication AS jour_date FROM Emploi
        UNION 
        SELECT DateAvis AS jour_date FROM Avis
    ) AS dt;
    
END
$$;

call sp_load_dim_temps();
--select * from dim_temps


CREATE OR REPLACE PROCEDURE sp_load_fact_proposition()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE FACT_Proposition;

    INSERT INTO FACT_Proposition (
        idSociete,
        idEmploi,
        id_temps,
        NbEmploi
    )
    SELECT
        e.idSociete,
        e.idEmploi,
        dt.id_temps,
        COUNT(*) AS NbEmploi  
    FROM
        Emploi AS e 
    JOIN 
        DIM_Temps AS dt ON e.DatePublication = dt.date
    GROUP BY
        e.idSociete,
        e.idEmploi,
        dt.id_temps;
END;
$$;


call sp_load_fact_proposition();
--select * from fact_proposition


CREATE OR REPLACE PROCEDURE sp_load_fact_avis()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE FACT_Avis;

    INSERT INTO FACT_Avis (
        idSociete,
        idAvis,
        id_temps,
        NoteMoyenneAvis,
        NbAvis
    )
    SELECT
        a.idSociete,
        a.idAvis,
        dt.id_temps,
        a.NoteMoyenneAvis, 
        1 AS NbAvis
    FROM
        Avis AS a
    JOIN
        DIM_Temps AS dt ON a.DateAvis = dt.date;
END;
$$;

call sp_load_fact_avis();