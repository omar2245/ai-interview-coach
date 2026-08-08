# JobFit Analysis

JobFit Analyzer compares one accepted resume with one job description and
produces a structured assessment that can optionally be retained locally.

## Language

**Analysis**:
One completed comparison of accepted resume text against an accepted job
description, including its structured assessment.
_Avoid_: Check, scan, AI response

**History Record**:
An immutable local copy of one successful Analysis, including its accepted
inputs, resume source metadata, structured assessment, and creation time.
_Avoid_: Saved result, database row, history item

**Resume Source**:
The origin of the accepted resume text: directly entered text or a parsed
uploaded file. It describes provenance; the original binary is not retained.
_Avoid_: File type, resume file

**Local History**:
The optional, single-user collection of History Records stored on the local
device. It is not an authenticated or multi-user data store.
_Avoid_: Account history, cloud history
