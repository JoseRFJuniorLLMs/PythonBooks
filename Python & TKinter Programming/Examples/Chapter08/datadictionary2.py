LC    = 1      # Lowercase Key
UC    = 2      # Uppercase Key
XX    = 3      # As Is
DT    = 4      # Date Insert
ND    = 5      # No Duplicate Keys
ZP    = 6      # Pad Zeroes
ZZ    = 7      # Do Not Display
ZS    = 8      # Do Not display, but fill in with key if blank

BLANKOK  = 0   # Blank is valid in this field
NONBLANK = 1   # Field cannot be blank

dataDict  = {
    'general': ('general',    0.11, 0.45, 0.075, [
        ('Employee #', 'employee_no', 9, XX, 'valid_blank', NONBLANK), 
        ('PIN', 'pin', 4, XX, '', BLANKOK),
        ('Category', 'type', 1, UC, 'valid_category', NONBLANK),
        ('SSN #', 'ssn', 9, XX, 'valid_ssn', BLANKOK),
        ('First Name', 'firstname', 12, XX, 'valid_blank', NONBLANK),
        ('Middle Name', 'middlename', 10, XX, '', BLANKOK),
        ('Last Name', 'lastname', 20, XX, 'valid_blank', NONBLANK),
        ('Status', 'status', 1, UC, '', BLANKOK),
        ('New Hire', 'newhire', 1, UC, 'valid_y_n_blank', BLANKOK),
        ('Seniority Date', 'senioritydate', 8, XX, 'valid_blank', NONBLANK),
        ('Seniority', 'seniority', 5, XX, 'valid_blank', NONBLANK),
        ('Base', 'base', 3, UC, 'valid_base', NONBLANK)],
        'General Information', [0]),
    'language': ('language',    0.11, 0.45, 0.075, [
        ('Language 1', 'lang1', 2, UC, 'valid_lang', BLANKOK),
        ('Language 2', 'lang2', 2, UC, 'valid_lang', BLANKOK),
        ('Language 3', 'lang3', 2, UC, 'valid_lang', BLANKOK),
        ('Language 4', 'lang4', 2, UC, 'valid_lang', BLANKOK),
        ('Language 5', 'lang5', 2, UC, 'valid_lang', BLANKOK),
        ('Language 6', 'lang6', 2, UC, 'valid_lang', BLANKOK)],
        'Languages', [0]),
    'crewqualifications': ('crewqualification',0.11,0.45,0.075, [
        ('Employee #', 'employee_no', 9, XX, '', BLANKOK), 
        ('Equipment', 'equipment', 3, UC, '', BLANKOK),
        ('Eqpt. Code', 'equipmentcode', 1, UC, '', BLANKOK),
        ('Position', 'position', 2, UC, '', BLANKOK),
        ('Pos. Code', 'positioncode', 2, UC, '', BLANKOK),
        ('Reserve', 'reserve', 1, UC, 'valid_r_blank', BLANKOK),
        ('Date of Hire', 'hiredate', 8, UC, '', BLANKOK),
        ('End Date', 'enddate', 8, UC, '', BLANKOK),                      
        ('Base Code', 'basecode', 1, UC, '', BLANKOK),
        ('Manager', 'manager', 1, UC, 'valid_y_n_blank', BLANKOK)],
        'Crew Qualifications', [0]
                           ) }

