import logging
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, expected_salary INTEGER, status TEXT)")


def addApplicant(name, role, expected_salary, status="applied"):
    conn.execute("INSERT INTO applicants (name, role, expected_salary, status) VALUES (?, ?, ?, ?)", (name, role, expected_salary, status))
    conn.commit()


def shortlist(role, salary_limit):
    rows = conn.execute("SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)).fetchall()
    limit = salary_limit
    total_seen = len(rows)
    result = []
    for name, salary in rows:
        if salary <= limit:
            result.append(name)
    if result:
        return result


def updateStatus(applicant_id, status):
    try:
        conn.execute("UPDATE applicants SET status = ? WHERE id = ?", (status, applicant_id))
        conn.commit()
    except sqlite3.Error as err:
        logging.error("Could not update applicant %s: %s", applicant_id, err)
        conn.rollback()
        return False
    return True

def exportReport(path):
    f = open(path, "w")
    for row in conn.execute("SELECT name, role, status FROM applicants"):
        f.write(",".join(row) + "\n")
    f.close()


def countByStatus(status):
    return conn.execute("SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)).fetchone()[0]


def main():
    addApplicant("Nina", "analyst", 600000)
    addApplicant("Omar", "analyst", 750000, "interview")
    addApplicant("Priya", "developer", 900000)
    updateStatus(1, "interview")
    print(shortlist("analyst", 500000 + 150000))
    exportReport("applicants_report.csv")
    print(countByStatus("interview"), "in interview")


main()