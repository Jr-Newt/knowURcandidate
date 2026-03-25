-- Know Your Candidate - Supabase Schema & Seed Data

-- Districts table
CREATE TABLE IF NOT EXISTS districts (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Constituencies table
CREATE TABLE IF NOT EXISTS constituencies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    district_id INTEGER REFERENCES districts(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name, district_id)
);

-- Candidates table
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    constituency_id INTEGER REFERENCES constituencies(id) ON DELETE CASCADE,
    party TEXT,
    education TEXT,
    criminal_cases INTEGER DEFAULT 0,
    serious_cases INTEGER DEFAULT 0,
    assets BIGINT DEFAULT 0,
    liabilities BIGINT DEFAULT 0,
    profession TEXT,
    age INTEGER,
    affidavit_link TEXT,
    -- Normalized scores (0.0 to 1.0)
    education_score REAL DEFAULT 0.0,
    criminal_score REAL DEFAULT 1.0,
    asset_score REAL DEFAULT 0.0,
    experience_score REAL DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name, constituency_id, party)
);

-- Candidate news table
CREATE TABLE IF NOT EXISTS candidate_news (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    source TEXT,
    published_date DATE,
    url TEXT UNIQUE NOT NULL,
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_constituencies_district ON constituencies(district_id);
CREATE INDEX IF NOT EXISTS idx_candidates_constituency ON candidates(constituency_id);
CREATE INDEX IF NOT EXISTS idx_candidate_news_candidate ON candidate_news(candidate_id);

-- =============================================
-- SEED DATA: Districts
-- =============================================
INSERT INTO districts (name) VALUES
    ('Thiruvananthapuram'), ('Kollam'), ('Pathanamthitta'), ('Alappuzha'),
    ('Kottayam'), ('Idukki'), ('Ernakulam'), ('Thrissur'),
    ('Palakkad'), ('Malappuram'), ('Kozhikode'), ('Wayanad'),
    ('Kannur'), ('Kasaragod')
ON CONFLICT (name) DO NOTHING;

-- =============================================
-- SEED DATA: Constituencies (sample subset)
-- =============================================

-- Thiruvananthapuram
INSERT INTO constituencies (name, district_id) VALUES
    ('Parassala', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Kovalam', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Neyyattinkara', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Attingal', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Thiruvananthapuram', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Nemom', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Kazhakkoottam', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Vattiyoorkavu', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Aruvikkara', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Nedumangad', (SELECT id FROM districts WHERE name='Thiruvananthapuram')),
    ('Vamanapuram', (SELECT id FROM districts WHERE name='Thiruvananthapuram'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Ernakulam
INSERT INTO constituencies (name, district_id) VALUES
    ('Perumbavoor', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Angamaly', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Aluva', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Kalamassery', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Paravur', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Vypeen', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Kochi', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Thrippunithura', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Ernakulam', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Thrikkakara', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Kunnathunad', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Piravom', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Muvattupuzha', (SELECT id FROM districts WHERE name='Ernakulam')),
    ('Kothamangalam', (SELECT id FROM districts WHERE name='Ernakulam'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Kozhikode
INSERT INTO constituencies (name, district_id) VALUES
    ('Kozhikode North', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Kozhikode South', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Beypore', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Elathur', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Kunnamangalam', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Koduvally', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Balussery', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Koyilandy', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Perambra', (SELECT id FROM districts WHERE name='Kozhikode')),
    ('Thiruvambady', (SELECT id FROM districts WHERE name='Kozhikode'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Kollam
INSERT INTO constituencies (name, district_id) VALUES
    ('Chadayamangalam', (SELECT id FROM districts WHERE name='Kollam')),
    ('Kundara', (SELECT id FROM districts WHERE name='Kollam')),
    ('Kollam', (SELECT id FROM districts WHERE name='Kollam')),
    ('Eravipuram', (SELECT id FROM districts WHERE name='Kollam')),
    ('Chathannoor', (SELECT id FROM districts WHERE name='Kollam')),
    ('Punalur', (SELECT id FROM districts WHERE name='Kollam')),
    ('Kunnathur', (SELECT id FROM districts WHERE name='Kollam')),
    ('Kottarakkara', (SELECT id FROM districts WHERE name='Kollam')),
    ('Pathanapuram', (SELECT id FROM districts WHERE name='Kollam')),
    ('Karunagappally', (SELECT id FROM districts WHERE name='Kollam'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Thrissur
INSERT INTO constituencies (name, district_id) VALUES
    ('Thrissur', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Nattika', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Kaipamangalam', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Irinjalakuda', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Puthukkad', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Chalakudy', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Kodungallur', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Kunnamkulam', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Guruvayoor', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Manalur', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Wadakkanchery', (SELECT id FROM districts WHERE name='Thrissur')),
    ('Ollur', (SELECT id FROM districts WHERE name='Thrissur'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Kannur
INSERT INTO constituencies (name, district_id) VALUES
    ('Kannur', (SELECT id FROM districts WHERE name='Kannur')),
    ('Dharmadam', (SELECT id FROM districts WHERE name='Kannur')),
    ('Thalassery', (SELECT id FROM districts WHERE name='Kannur')),
    ('Kuthuparamba', (SELECT id FROM districts WHERE name='Kannur')),
    ('Mattannur', (SELECT id FROM districts WHERE name='Kannur')),
    ('Peravoor', (SELECT id FROM districts WHERE name='Kannur')),
    ('Taliparamba', (SELECT id FROM districts WHERE name='Kannur')),
    ('Irikkur', (SELECT id FROM districts WHERE name='Kannur')),
    ('Azhikode', (SELECT id FROM districts WHERE name='Kannur')),
    ('Payyannur', (SELECT id FROM districts WHERE name='Kannur')),
    ('Kalliasseri', (SELECT id FROM districts WHERE name='Kannur'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Palakkad
INSERT INTO constituencies (name, district_id) VALUES
    ('Chittur', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Palakkad', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Tarur', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Shornur', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Ottapalam', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Kongad', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Mannarkkad', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Malampuzha', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Pattambi', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Thrithala', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Alathur', (SELECT id FROM districts WHERE name='Palakkad')),
    ('Nenmara', (SELECT id FROM districts WHERE name='Palakkad'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Malappuram
INSERT INTO constituencies (name, district_id) VALUES
    ('Manjeri', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Perinthalmanna', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Mankada', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Malappuram', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Vengara', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Vallikkunnu', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Tirurangadi', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Tanur', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Tirur', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Kottakkal', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Thavanur', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Ponnani', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Kondotty', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Nilambur', (SELECT id FROM districts WHERE name='Malappuram')),
    ('Wandoor', (SELECT id FROM districts WHERE name='Malappuram'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Pathanamthitta
INSERT INTO constituencies (name, district_id) VALUES
    ('Thiruvalla', (SELECT id FROM districts WHERE name='Pathanamthitta')),
    ('Ranni', (SELECT id FROM districts WHERE name='Pathanamthitta')),
    ('Aranmula', (SELECT id FROM districts WHERE name='Pathanamthitta')),
    ('Konni', (SELECT id FROM districts WHERE name='Pathanamthitta')),
    ('Adoor', (SELECT id FROM districts WHERE name='Pathanamthitta'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Alappuzha
INSERT INTO constituencies (name, district_id) VALUES
    ('Kayamkulam', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Mavelikkara', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Chengannur', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Alappuzha', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Ambalapuzha', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Haripad', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Kuttanad', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Aroor', (SELECT id FROM districts WHERE name='Alappuzha')),
    ('Cherthala', (SELECT id FROM districts WHERE name='Alappuzha'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Kottayam
INSERT INTO constituencies (name, district_id) VALUES
    ('Changanassery', (SELECT id FROM districts WHERE name='Kottayam')),
    ('Kottayam', (SELECT id FROM districts WHERE name='Kottayam')),
    ('Puthuppally', (SELECT id FROM districts WHERE name='Kottayam')),
    ('Pala', (SELECT id FROM districts WHERE name='Kottayam')),
    ('Kaduthuruthy', (SELECT id FROM districts WHERE name='Kottayam')),
    ('Ettumanoor', (SELECT id FROM districts WHERE name='Kottayam'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Idukki
INSERT INTO constituencies (name, district_id) VALUES
    ('Thodupuzha', (SELECT id FROM districts WHERE name='Idukki')),
    ('Idukki', (SELECT id FROM districts WHERE name='Idukki')),
    ('Devikulam', (SELECT id FROM districts WHERE name='Idukki')),
    ('Udumbanchola', (SELECT id FROM districts WHERE name='Idukki')),
    ('Peerumedu', (SELECT id FROM districts WHERE name='Idukki'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Wayanad
INSERT INTO constituencies (name, district_id) VALUES
    ('Mananthavady', (SELECT id FROM districts WHERE name='Wayanad')),
    ('Sulthanbathery', (SELECT id FROM districts WHERE name='Wayanad')),
    ('Kalpetta', (SELECT id FROM districts WHERE name='Wayanad'))
ON CONFLICT (name, district_id) DO NOTHING;

-- Kasaragod
INSERT INTO constituencies (name, district_id) VALUES
    ('Manjeshwar', (SELECT id FROM districts WHERE name='Kasaragod')),
    ('Kasaragod', (SELECT id FROM districts WHERE name='Kasaragod')),
    ('Udma', (SELECT id FROM districts WHERE name='Kasaragod')),
    ('Kanhangad', (SELECT id FROM districts WHERE name='Kasaragod')),
    ('Thrikkaripur', (SELECT id FROM districts WHERE name='Kasaragod'))
ON CONFLICT (name, district_id) DO NOTHING;

-- =============================================
-- SEED DATA: Sample Candidates (realistic mock data)
-- =============================================

-- Thiruvananthapuram constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('V.S. Sunil Kumar', (SELECT id FROM constituencies WHERE name='Thiruvananthapuram' AND district_id=(SELECT id FROM districts WHERE name='Thiruvananthapuram')), 'CPI(M)', 'Post Graduate', 2, 0, 45000000, 1200000, 'Political Worker', 58, 0.8, 0.75, 0.55, 0.8, 'https://affidavit.eci.gov.in/'),
    ('Shashi Tharoor', (SELECT id FROM constituencies WHERE name='Thiruvananthapuram' AND district_id=(SELECT id FROM districts WHERE name='Thiruvananthapuram')), 'INC', 'Doctorate', 0, 0, 120000000, 5000000, 'Author / Diplomat', 67, 1.0, 1.0, 0.75, 0.95, 'https://affidavit.eci.gov.in/'),
    ('Kummanam Rajasekharan', (SELECT id FROM constituencies WHERE name='Thiruvananthapuram' AND district_id=(SELECT id FROM districts WHERE name='Thiruvananthapuram')), 'BJP', 'Graduate', 1, 0, 35000000, 800000, 'Social Worker', 63, 0.6, 0.85, 0.45, 0.7, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Nemom constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('O. Rajagopal', (SELECT id FROM constituencies WHERE name='Nemom' AND district_id=(SELECT id FROM districts WHERE name='Thiruvananthapuram')), 'BJP', 'Law Graduate', 0, 0, 27000000, 500000, 'Advocate', 75, 0.7, 1.0, 0.4, 0.9, 'https://affidavit.eci.gov.in/'),
    ('K. Muraleedharan', (SELECT id FROM constituencies WHERE name='Nemom' AND district_id=(SELECT id FROM districts WHERE name='Thiruvananthapuram')), 'INC', 'Graduate', 3, 1, 55000000, 2000000, 'Politician', 62, 0.6, 0.5, 0.6, 0.85, 'https://affidavit.eci.gov.in/'),
    ('V. Sivankutty', (SELECT id FROM constituencies WHERE name='Nemom' AND district_id=(SELECT id FROM districts WHERE name='Thiruvananthapuram')), 'CPI(M)', 'Post Graduate', 1, 0, 18000000, 300000, 'Teacher / Politician', 55, 0.8, 0.85, 0.3, 0.75, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Kochi constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('K.J. Maxi', (SELECT id FROM constituencies WHERE name='Kochi' AND district_id=(SELECT id FROM districts WHERE name='Ernakulam')), 'INC', 'Post Graduate', 0, 0, 32000000, 1500000, 'Business / Politician', 56, 0.8, 1.0, 0.45, 0.7, 'https://affidavit.eci.gov.in/'),
    ('Geetha Suresh', (SELECT id FROM constituencies WHERE name='Kochi' AND district_id=(SELECT id FROM districts WHERE name='Ernakulam')), 'CPI(M)', 'Graduate', 1, 0, 15000000, 200000, 'Teacher', 48, 0.6, 0.85, 0.25, 0.5, 'https://affidavit.eci.gov.in/'),
    ('K.P. Prakash Babu', (SELECT id FROM constituencies WHERE name='Kochi' AND district_id=(SELECT id FROM districts WHERE name='Ernakulam')), 'BJP', 'Post Graduate', 0, 0, 8000000, 100000, 'Social Worker', 52, 0.8, 1.0, 0.15, 0.55, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Thrikkakara constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('Uma Thomas', (SELECT id FROM constituencies WHERE name='Thrikkakara' AND district_id=(SELECT id FROM districts WHERE name='Ernakulam')), 'INC', 'Post Graduate', 0, 0, 42000000, 3000000, 'Activist / Politician', 50, 0.8, 1.0, 0.52, 0.6, 'https://affidavit.eci.gov.in/'),
    ('Joe Joseph', (SELECT id FROM constituencies WHERE name='Thrikkakara' AND district_id=(SELECT id FROM districts WHERE name='Ernakulam')), 'CPI(M)', 'Doctorate', 0, 0, 25000000, 1000000, 'Professor', 55, 1.0, 1.0, 0.38, 0.7, 'https://affidavit.eci.gov.in/'),
    ('A.N. Radhakrishnan', (SELECT id FROM constituencies WHERE name='Thrikkakara' AND district_id=(SELECT id FROM districts WHERE name='Ernakulam')), 'BJP', 'Graduate', 2, 1, 60000000, 5000000, 'Business', 60, 0.6, 0.5, 0.65, 0.65, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Kozhikode South constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('Ahammed Devarkovil', (SELECT id FROM constituencies WHERE name='Kozhikode South' AND district_id=(SELECT id FROM districts WHERE name='Kozhikode')), 'CPI(M)', 'Graduate', 1, 0, 22000000, 800000, 'Political Worker', 50, 0.6, 0.85, 0.35, 0.6, 'https://affidavit.eci.gov.in/'),
    ('Noorbina Rasheed', (SELECT id FROM constituencies WHERE name='Kozhikode South' AND district_id=(SELECT id FROM districts WHERE name='Kozhikode')), 'INC', 'Post Graduate', 0, 0, 18000000, 400000, 'Journalist / Writer', 55, 0.8, 1.0, 0.3, 0.65, 'https://affidavit.eci.gov.in/'),
    ('M.T. Ramesh', (SELECT id FROM constituencies WHERE name='Kozhikode South' AND district_id=(SELECT id FROM districts WHERE name='Kozhikode')), 'BJP', 'Graduate', 4, 2, 12000000, 200000, 'Political Worker', 58, 0.6, 0.3, 0.22, 0.6, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Thrissur constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('P. Balachandran', (SELECT id FROM constituencies WHERE name='Thrissur' AND district_id=(SELECT id FROM districts WHERE name='Thrissur')), 'CPI(M)', 'Post Graduate', 0, 0, 28000000, 1000000, 'Politician', 60, 0.8, 1.0, 0.4, 0.8, 'https://affidavit.eci.gov.in/'),
    ('Padmaja Venugopal', (SELECT id FROM constituencies WHERE name='Thrissur' AND district_id=(SELECT id FROM districts WHERE name='Thrissur')), 'INC', 'Graduate', 0, 0, 50000000, 2000000, 'Social Worker', 52, 0.6, 1.0, 0.58, 0.5, 'https://affidavit.eci.gov.in/'),
    ('Suresh Gopi', (SELECT id FROM constituencies WHERE name='Thrissur' AND district_id=(SELECT id FROM districts WHERE name='Thrissur')), 'BJP', 'Post Graduate', 1, 0, 150000000, 8000000, 'Actor / Politician', 65, 0.8, 0.85, 0.9, 0.4, 'https://affidavit.eci.gov.in/'),
    ('Rajya Lakshmi', (SELECT id FROM constituencies WHERE name='Thrissur' AND district_id=(SELECT id FROM districts WHERE name='Thrissur')), 'AAP', 'Doctorate', 0, 0, 5000000, 100000, 'Doctor', 42, 1.0, 1.0, 0.1, 0.3, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Kannur constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('E.P. Jayarajan', (SELECT id FROM constituencies WHERE name='Dharmadam' AND district_id=(SELECT id FROM districts WHERE name='Kannur')), 'CPI(M)', 'SSLC', 5, 2, 38000000, 1500000, 'Political Worker', 67, 0.2, 0.2, 0.48, 0.85, 'https://affidavit.eci.gov.in/'),
    ('Pinarayi Vijayan', (SELECT id FROM constituencies WHERE name='Dharmadam' AND district_id=(SELECT id FROM districts WHERE name='Kannur')), 'CPI(M)', 'Graduate', 3, 1, 25000000, 500000, 'Politician', 78, 0.6, 0.5, 0.38, 0.95, 'https://affidavit.eci.gov.in/'),
    ('C.K. Padmanabhan', (SELECT id FROM constituencies WHERE name='Dharmadam' AND district_id=(SELECT id FROM districts WHERE name='Kannur')), 'INC', 'Post Graduate', 0, 0, 15000000, 300000, 'Advocate', 55, 0.8, 1.0, 0.25, 0.6, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- Palakkad constituency candidates
INSERT INTO candidates (name, constituency_id, party, education, criminal_cases, serious_cases, assets, liabilities, profession, age, education_score, criminal_score, asset_score, experience_score, affidavit_link) VALUES
    ('Shafi Parambil', (SELECT id FROM constituencies WHERE name='Palakkad' AND district_id=(SELECT id FROM districts WHERE name='Palakkad')), 'INC', 'Graduate', 0, 0, 20000000, 600000, 'Politician', 42, 0.6, 1.0, 0.32, 0.5, 'https://affidavit.eci.gov.in/'),
    ('C. Krishnakumar', (SELECT id FROM constituencies WHERE name='Palakkad' AND district_id=(SELECT id FROM districts WHERE name='Palakkad')), 'BJP', 'Post Graduate', 1, 0, 35000000, 1000000, 'Business / Politician', 55, 0.8, 0.85, 0.45, 0.6, 'https://affidavit.eci.gov.in/'),
    ('Sarin P.', (SELECT id FROM constituencies WHERE name='Palakkad' AND district_id=(SELECT id FROM districts WHERE name='Palakkad')), 'CPI(M)', 'Post Graduate', 0, 0, 12000000, 200000, 'Teacher', 38, 0.8, 1.0, 0.22, 0.35, 'https://affidavit.eci.gov.in/')
ON CONFLICT (name, constituency_id, party) DO NOTHING;

-- =============================================
-- SEED DATA: Sample News Articles
-- =============================================
INSERT INTO candidate_news (candidate_id, title, source, published_date, url, summary) VALUES
    ((SELECT id FROM candidates WHERE name='Shashi Tharoor' LIMIT 1), 'Tharoor Campaigns on Development Agenda for Thiruvananthapuram', 'The Hindu', '2025-12-15', 'https://example.com/news/tharoor-development-1', 'Shashi Tharoor outlined his development plans focusing on IT corridor expansion and metro connectivity.'),
    ((SELECT id FROM candidates WHERE name='Shashi Tharoor' LIMIT 1), 'Tharoor Addresses Education Reform at Rally', 'Manorama Online', '2025-11-20', 'https://example.com/news/tharoor-education-1', 'Former diplomat emphasized the need for modernizing Kerala''s education system.'),
    ((SELECT id FROM candidates WHERE name='Shashi Tharoor' LIMIT 1), 'Asset Declaration Shows Tharoor Among Wealthiest Candidates', 'NDTV', '2026-01-10', 'https://example.com/news/tharoor-assets-1', 'Election affidavit reveals assets worth over Rs 12 crore.'),
    ((SELECT id FROM candidates WHERE name='Suresh Gopi' LIMIT 1), 'Suresh Gopi Files Nomination from Thrissur', 'India Today', '2026-01-05', 'https://example.com/news/sureshgopi-nomination-1', 'Actor-turned-politician files nomination papers for the Thrissur assembly constituency.'),
    ((SELECT id FROM candidates WHERE name='Suresh Gopi' LIMIT 1), 'Suresh Gopi Promises Cultural Revival in Thrissur', 'Mathrubhumi', '2025-12-28', 'https://example.com/news/sureshgopi-culture-1', 'BJP candidate promises to restore Thrissur''s cultural heritage and boost tourism.'),
    ((SELECT id FROM candidates WHERE name='Pinarayi Vijayan' LIMIT 1), 'CM Vijayan Seeks Re-election from Dharmadam', 'The Hindu', '2026-01-12', 'https://example.com/news/vijayan-dharmadam-1', 'Chief Minister Pinarayi Vijayan announces candidacy from Dharmadam constituency.'),
    ((SELECT id FROM candidates WHERE name='Pinarayi Vijayan' LIMIT 1), 'Vijayan Highlights Welfare Schemes Achievements', 'Deccan Herald', '2025-12-01', 'https://example.com/news/vijayan-welfare-1', 'CM points to social welfare and infrastructure development during his tenure.'),
    ((SELECT id FROM candidates WHERE name='Pinarayi Vijayan' LIMIT 1), 'Opposition Questions Vijayan on Pending Criminal Cases', 'Indian Express', '2026-02-05', 'https://example.com/news/vijayan-cases-1', 'Congress demands explanation on criminal cases pending against the Chief Minister.'),
    ((SELECT id FROM candidates WHERE name='Uma Thomas' LIMIT 1), 'Uma Thomas Wins Hearts in Thrikkakara Campaign', 'Manorama Online', '2026-01-20', 'https://example.com/news/umathomas-campaign-1', 'INC candidate Uma Thomas seen as strong contender in the Thrikkakara by-election.'),
    ((SELECT id FROM candidates WHERE name='Shafi Parambil' LIMIT 1), 'Youth Leader Shafi Parambil Energizes Palakkad Campaign', 'The News Minute', '2026-02-01', 'https://example.com/news/shafi-campaign-1', 'Young INC leader draws large crowds with promises of jobs and development.')
ON CONFLICT (url) DO NOTHING;
