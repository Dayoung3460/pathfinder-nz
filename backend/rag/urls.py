"""INZ document URLs for ingestion into ChromaDB.

All URLs are sourced from official Immigration New Zealand pages.
Update this file when INZ restructures or moves pages.
"""

EMPLOYER_URLS = [
    "https://www.immigration.govt.nz/work/for-employers/",
    "https://www.immigration.govt.nz/work/for-employers/hiring-people-from-overseas/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/",
    "https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa",
    "https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa/accreditation-types-and-employers-requirements",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/aewv-employer-accreditation-and-job-check-process/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/applying-for-a-job-check-process-steps/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/applying-for-a-job-check-process-steps/how-we-calculate-pay-rates-for-the-aewv/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/applying-for-a-job-check-process-steps/engaging-with-work-and-income-before-your-job-check/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/recruiting-and-supporting-a-migrant-to-apply-for-an-aewv-process-steps/",
    "https://www.immigration.govt.nz/work/for-employers/getting-accreditation-or-approval-to-hire/employer-accreditation-for-the-aewv/recruiting-and-supporting-a-migrant-to-apply-for-an-aewv-process-steps/check-if-a-migrant-applicant-is-suitably-qualified-for-an-aewv/",
    "https://www.immigration.govt.nz/work/for-employers/hiring-people-from-overseas/making-a-job-offer/",
    "https://www.immigration.govt.nz/about-us/news-centre/accredited-employer-work-visa-aewv-key-information-and-statistics/",
    "https://www.immigration.govt.nz/about-us/news-centre/how-changes-to-the-accredited-employer-work-visa-aewv-may-affect-you/",
    "https://www.immigration.govt.nz/employ-migrants/new-employer-accreditation-and-work-visa/passing-the-job-check/sector-agreements-and-hiring-migrants-on-an-aewv",
    "https://www.immigration.govt.nz/about-us/news-centre/changes-to-the-accredited-employer-work-visa-aewv/",
    "https://www.immigration.govt.nz/about-us/news-centre/changes-to-the-accredited-employer-work-visa-aewv-and-median-wage/",
    "https://www.immigration.govt.nz/about-us/news-centre/changes-to-accredited-employer-work-visa-aewv-form-questions-for-green-list-occupations-and-wage-thresholds/",
    "https://www.immigration.govt.nz/about-us/news-centre/recognising-new-national-occupation-list-nol-occupations-in-the-accredited-employer-work-visa-aewv/",
    "https://www.immigration.govt.nz/new-zealand-visas/preparing-a-visa-application/working-in-nz/wage-rate-requirements-for-visas",
]

AEWV_URLS = [
    "https://www.immigration.govt.nz/visas/accredited-employer-work-visa/",
    "https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-work-visa",
    "https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions",
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/approved-employers/accredited-employer-list/",
]

SMC_URLS = [
    "https://www.immigration.govt.nz/visas/skilled-migrant-category-resident-visa/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/skilled-migrant-category-pathway-to-residence/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/skilled-migrant-category-pathway-to-residence/pay-rates-for-the-skilled-migrant-category-resident-visa/",
    "https://www.immigration.govt.nz/formshelp/smc-eoi-form",
    "https://www.immigration.govt.nz/formshelp/smc-visa-application",
    "https://www.immigration.govt.nz/about-us/news-centre/further-changes-to-the-skilled-migrant-category-to-come-into-effect-in-august-2026/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/",
    "https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/interim-visas-so-you-can-stay-here-lawfully/skilled-migrant-category-interim-visa/",
]

PARTNER_URLS = [
    "https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/partnership-and-how-to-prove-it/",
    "https://www.immigration.govt.nz/about-us/news-centre/partnership-visas/",
    "https://www.immigration.govt.nz/visas/partner-of-a-new-zealander-resident-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-new-zealander-work-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-new-zealander-visitor-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-student-work-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-student-visitor-visa/",
    "https://www.immigration.govt.nz/visas/partner-of-a-worker-work-visa/",
]

STUDENT_URLS = [
    "https://www.immigration.govt.nz/study/study-visas/",
    "https://www.immigration.govt.nz/assist-migrants-and-students/assist-students/student-visa-info",
    "https://www.immigration.govt.nz/study/once-you-have-a-student-visa/check-or-change-your-student-visa-conditions/",
    "https://www.immigration.govt.nz/about-us/news-centre/upcoming-changes-to-student-visa-work-rights/",
    "https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/bringing-family-on-a-student-visa/",
]

VOC_URLS = [
    "https://www.immigration.govt.nz/new-zealand-visas/already-have-a-visa/your-visa-conditions/variation-of-conditions-temporary-visas/varying-a-visitor-visa",
    "https://www.immigration.govt.nz/formshelp/application-for-a-variation-of-conditions-student",
]

VISITOR_URLS = [
    "https://www.immigration.govt.nz/visas/visitor-visa",
]

WORKING_HOLIDAY_URLS = [
    "https://www.immigration.govt.nz/work/working-holiday-visas/",
]

POST_STUDY_WORK_URLS = [
    "https://www.immigration.govt.nz/visas/post-study-work-visa",
]

HEALTH_CHARACTER_URLS = []

FEES_URLS = []

PROCESSING_TIMES_URLS = [
    "https://www.immigration.govt.nz/new-zealand-visas/waiting-for-a-visa/how-long-it-takes-to-process-your-visa-application",
]

ENGLISH_LANGUAGE_URLS = []

ESSENTIAL_SKILLS_URLS = [
    "https://www.immigration.govt.nz/visas/essential-skills-work-visa",
]

RESIDENCE_URLS = [
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/",
]

FAMILY_URLS = [
    "https://www.immigration.govt.nz/visas/parent-retirement-resident-visa",
    "https://www.immigration.govt.nz/process-to-apply/once-you-have-a-visa/bringing-family-to-new-zealand/dependent-children/",
]

APPLICATION_PROCESS_URLS = [
    "https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/",
]

REFUGEE_URLS = []

ENTREPRENEUR_INVESTOR_URLS = [
    "https://www.immigration.govt.nz/visas/entrepreneur-work-visa",
    "https://www.immigration.govt.nz/visas/entrepreneur-resident-visa/",
]

TRANSIT_URLS = [
    "https://www.immigration.govt.nz/visas/transit-visa",
]

OVERSTAY_URLS = []

ADVISER_URLS = []

GREEN_LIST_URLS = [
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/green-list-occupations-qualifications-and-skills/green-list-roles-jobs-we-need-people-for-in-new-zealand/",
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/green-list-occupations-qualifications-and-skills/",
    "https://www.immigration.govt.nz/visas/straight-to-residence-visa/",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/green-list-pathway-to-residence/",
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/green-list-occupations-qualifications-and-skills/check-if-you-need-an-international-qualification-assessment/",
    "https://www.immigration.govt.nz/about-us/news-centre/green-list-and-other-immigration-changes/",
    "https://www.immigration.govt.nz/about-us/news-centre/ten-trades-occupations-to-be-added-to-the-work-to-residence-pathway/",
    "https://www.immigration.govt.nz/new-zealand-visas/preparing-a-visa-application/working-in-nz/qualifications-for-work/green-list-occupations",
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/green-list-occupations-qualifications-and-skills/find-your-anzsco-skill-level/",
    "https://www.immigration.govt.nz/work/requirements-for-work-visas/green-list-occupations-qualifications-and-skills/national-occupation-list-occupations-used-for-an-aewv/",
    "https://www.immigration.govt.nz/visas/work-to-residence-visa/",
    "https://www.immigration.govt.nz/new-zealand-visas/preparing-a-visa-application/working-in-nz/qualifications-for-work/care-workforce-work-to-residence-visa-requirements-and-roles",
    "https://www.immigration.govt.nz/live/resident-visas-to-live-in-new-zealand/skilled-residence-pathways-in-new-zealand/getting-new-zealand-residence-based-on-your-skills/",
    "https://www.immigration.govt.nz/about-us/news-centre/overview-of-skilled-residence-pathways/",
]

GENERAL_URLS = [
    "https://www.immigration.govt.nz/new-zealand-visas/preparing-a-visa-application/character-and-identity/good-character/supporting-partner-character",
    "https://www.immigration.govt.nz/process-to-apply/waiting-for-a-visa/interim-visas-so-you-can-stay-here-lawfully/interim-visa-conditions/",
]

_ALL_URLS_RAW = (
    EMPLOYER_URLS
    + AEWV_URLS
    + SMC_URLS
    + PARTNER_URLS
    + STUDENT_URLS
    + VOC_URLS
    + VISITOR_URLS
    + WORKING_HOLIDAY_URLS
    + POST_STUDY_WORK_URLS
    + HEALTH_CHARACTER_URLS
    + FEES_URLS
    + PROCESSING_TIMES_URLS
    + ENGLISH_LANGUAGE_URLS
    + ESSENTIAL_SKILLS_URLS
    + RESIDENCE_URLS
    + FAMILY_URLS
    + APPLICATION_PROCESS_URLS
    + REFUGEE_URLS
    + ENTREPRENEUR_INVESTOR_URLS
    + TRANSIT_URLS
    + OVERSTAY_URLS
    + ADVISER_URLS
    + GREEN_LIST_URLS
    + GENERAL_URLS
)

# Auto-deduplicate while preserving order
ALL_URLS = list(dict.fromkeys(_ALL_URLS_RAW))
