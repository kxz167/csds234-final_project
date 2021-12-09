-- TABLES:
CREATE TABLE department (
    id INT,
    name TEXT,
    abbreviation TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE course (
    id INT,
    code INT,
    department_id INT,
    name TEXT,
    credits INT4RANGE,
    description TEXT,
    standing_prequisite TEXT,
    standing_recommendation TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (department_id)
        REFERENCES department (id)
        ON DELETE CASCADE
);

CREATE TABLE course_prerequisite (
    course_id INT, 
    prerequisite_id INT,
    PRIMARY KEY (course_id, prerequisite_id),
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE course_recommendation (
    course_id INT, 
    recommendation_id INT,
    PRIMARY KEY (course_id, recommendation_id),
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE,
    FOREIGN KEY (recommendation_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE csbs_suggested_plan (
    id INT,
    course_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE csba_suggested_plan (
    id INT,
    course_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE dsbs_suggested_plan (
    id INT,
    course_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE cs_breadth(
    course_id INT,
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE cs_depth(
    course_id INT,
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

CREATE TABLE cs_technical(
    course_id INT,
    FOREIGN KEY (course_id)
        REFERENCES course (id)
        ON DELETE CASCADE
);

-- INSERTION OF CSV:
\COPY department FROM 'Z:\csds234\final_project\heroku_app\_database\department.csv' CSV HEADER;
\COPY course FROM 'Z:\csds234\final_project\heroku_app\_database\course.csv' CSV HEADER;
\COPY course_prerequisite FROM 'Z:\csds234\final_project\heroku_app\_database\course_prerequisite.csv' CSV;
\COPY course_recommendation FROM 'Z:\csds234\final_project\heroku_app\_database\course_recommendation.csv' CSV HEADER;
\COPY csbs_suggested_plan FROM 'Z:\csds234\final_project\heroku_app\_database\csbs_suggested_plan.csv' CSV HEADER;
\COPY csba_suggested_plan FROM 'Z:\csds234\final_project\heroku_app\_database\csba_suggested_plan.csv' CSV HEADER;
\COPY dsbs_suggested_plan FROM 'Z:\csds234\final_project\heroku_app\_database\dsbs_suggested_plan.csv' CSV HEADER;
\COPY cs_breadth FROM 'Z:\csds234\final_project\heroku_app\_database\cs_breadth.csv' CSV HEADER;
\COPY cs_depth FROM 'Z:\csds234\final_project\heroku_app\_database\cs_depth.csv' CSV HEADER;
\COPY cs_technical FROM 'Z:\csds234\final_project\heroku_app\_database\cs_technical.csv' CSV HEADER;
