DROP TABLE IF EXISTS facility;

CREATE TABLE facility (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    url TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    country TEXT,
    locality TEXT,
    region TEXT,
    postal_code TEXT,
    street_address TEXT
);

-- Insert 100 sample rows
INSERT INTO facility (name, phone, url, latitude, longitude, country, locality, region, postal_code, street_address)
SELECT
    'Facility ' || g,
    '+1-555-01' || LPAD(g::TEXT, 2, '0'),
    'https://facility' || g || '.example.com',
    37.0 + random(),                      -- Random latitude between 37.0–38.0
    -122.0 + random(),                   -- Random longitude between -122.0–-121.0
    'US',
    'City ' || (g % 10),
    'Region ' || (g % 5),
    'ZIP' || LPAD((90000 + g)::TEXT, 5, '0'),
    (100 + g) || ' Main St'
FROM generate_series(1, 100) AS g;
