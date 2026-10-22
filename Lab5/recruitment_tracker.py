"""Applicant tracking system for an HR team.

Stores job applicants in an in-memory SQLite database, shortlists candidates
for a role against a salary budget, updates hiring status and exports a report.
"""
import csv
import logging
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, "
    "expected_salary INTEGER, status TEXT)"
)


def add_applicant(name, role, expected_salary, status="applied"):
    """Insert a new applicant using a parameterised query."""
    conn.execute(
        "INSERT INTO applicants (name, role, expected_salary, status) VALUES (?, ?, ?, ?)",
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(role, salary_limit):
    """Return names of applicants for `role` whose expected salary fits the limit."""
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)
    ).fetchall()
    return [name for name, salary in rows if salary <= salary_limit]


def update_status(applicant_id, status):
    """Update an applicant's hiring status. Return True on success, False on failure."""
    try:
        conn.execute("UPDATE applicants SET status = ? WHERE id = ?", (status, applicant_id))
        conn.commit()
    except sqlite3.Error as err:
        logging.error("Could not update applicant %s: %s", applicant_id, err)
        conn.rollback()
        return False
    return True


def export_report(path):
    """Write name, role and status of every applicant to a CSV file."""
    with open(path, "w", encoding="utf-8", newline="") as report_file:
        writer = csv.writer(report_file)
        writer.writerows(conn.execute("SELECT name, role, status FROM applicants"))


def count_by_status(status):
    """Return how many applicants currently have the given status."""
    return conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)
    ).fetchone()[0]


def main():
    """Run a short demonstration of the tracker."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)
    update_status(1, "interview")
    print(shortlist("analyst", 500000 + 150000))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()
