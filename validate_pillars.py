#!/usr/bin/env python3
"""
TAC Architecture Validation Script
===================================
Checks pillars.json for common errors:
- Duplicate IDs
- Missing required fields
- Orphaned items (children without parents)
- Similar titles (possible overlap)

HOW TO USE:
1. Put this file in your repo root (next to data/ folder)
2. Run: python validate_pillars.py
3. It will print any problems it finds

No coding knowledge needed - just run it and read the output!
"""

import json
import sys
from collections import Counter

# ============================================
# CONFIGURATION - What fields are required?
# ============================================

REQUIRED_PILLAR_FIELDS = ["id", "title", "definition", "inclusion_tests", "exclusion_tests", "sub_pillars"]
REQUIRED_SUBPILLAR_FIELDS = ["id", "title", "definition", "branches"]
REQUIRED_BRANCH_FIELDS = ["id", "title", "definition", "lens", "topic_domains"]
REQUIRED_TOPICDOMAIN_FIELDS = ["id", "title", "definition"]


def load_pillars(filepath="data/pillars.json"):
    """Load the pillars.json file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find {filepath}")
        print("   Make sure you're running this from the repo root folder")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in {filepath}")
        print(f"   {e}")
        sys.exit(1)


def check_required_fields(item, required_fields, item_type, item_id):
    """Check if an item has all required fields"""
    errors = []
    for field in required_fields:
        if field not in item:
            errors.append(f"❌ {item_type} '{item_id}' is missing required field: {field}")
        elif item[field] is None or item[field] == "":
            errors.append(f"⚠️  {item_type} '{item_id}' has empty field: {field}")
    return errors


def check_duplicate_ids(all_ids):
    """Check for duplicate IDs"""
    errors = []
    id_counts = Counter(all_ids)
    for id_val, count in id_counts.items():
        if count > 1:
            errors.append(f"❌ DUPLICATE ID: '{id_val}' appears {count} times!")
    return errors


def check_id_format(item_id, expected_prefix, item_type):
    """Check if ID follows expected format"""
    errors = []
    if not item_id.startswith(expected_prefix):
        errors.append(f"⚠️  {item_type} ID '{item_id}' doesn't start with expected prefix '{expected_prefix}'")
    return errors


def find_similar_titles(titles_with_ids, threshold=0.6):
    """Find titles that might be too similar (possible overlap)"""
    warnings = []
    
    # Simple word overlap check
    for i, (id1, title1) in enumerate(titles_with_ids):
        words1 = set(title1.lower().split())
        for id2, title2 in titles_with_ids[i+1:]:
            words2 = set(title2.lower().split())
            
            # Calculate overlap
            if len(words1) > 0 and len(words2) > 0:
                overlap = len(words1 & words2) / min(len(words1), len(words2))
                if overlap >= threshold:
                    warnings.append(
                        f"⚠️  POSSIBLE OVERLAP: '{title1}' ({id1}) and '{title2}' ({id2}) "
                        f"share {int(overlap*100)}% of words"
                    )
    
    return warnings


def validate_pillars(data):
    """Main validation function"""
    errors = []
    warnings = []
    all_ids = []
    all_topic_domain_titles = []
    
    stats = {
        "pillars": 0,
        "sub_pillars": 0,
        "branches": 0,
        "topic_domains": 0
    }
    
    pillars = data.get("pillars", [])
    
    if not pillars:
        warnings.append("⚠️  No pillars found in file (pillars array is empty)")
        return errors, warnings, stats
    
    for pillar in pillars:
        pillar_id = pillar.get("id", "UNKNOWN")
        stats["pillars"] += 1
        all_ids.append(pillar_id)
        
        # Check pillar fields
        errors.extend(check_required_fields(pillar, REQUIRED_PILLAR_FIELDS, "Pillar", pillar_id))
        
        # Check sub-pillars
        sub_pillars = pillar.get("sub_pillars", [])
        for sp in sub_pillars:
            sp_id = sp.get("id", "UNKNOWN")
            stats["sub_pillars"] += 1
            all_ids.append(sp_id)
            
            errors.extend(check_required_fields(sp, REQUIRED_SUBPILLAR_FIELDS, "Sub-Pillar", sp_id))
            errors.extend(check_id_format(sp_id, pillar_id + ".", "Sub-Pillar"))
            
            # Check branches
            branches = sp.get("branches", [])
            for branch in branches:
                branch_id = branch.get("id", "UNKNOWN")
                stats["branches"] += 1
                all_ids.append(branch_id)
                
                errors.extend(check_required_fields(branch, REQUIRED_BRANCH_FIELDS, "Branch", branch_id))
                errors.extend(check_id_format(branch_id, sp_id + ".", "Branch"))
                
                # Check topic domains
                topic_domains = branch.get("topic_domains", [])
                for td in topic_domains:
                    td_id = td.get("id", "UNKNOWN")
                    td_title = td.get("title", "")
                    stats["topic_domains"] += 1
                    all_ids.append(td_id)
                    all_topic_domain_titles.append((td_id, td_title))
                    
                    errors.extend(check_required_fields(td, REQUIRED_TOPICDOMAIN_FIELDS, "Topic Domain", td_id))
    
    # Check for duplicate IDs
    errors.extend(check_duplicate_ids(all_ids))
    
    # Check for similar topic domain titles (possible overlap)
    if len(all_topic_domain_titles) > 1:
        warnings.extend(find_similar_titles(all_topic_domain_titles))
    
    return errors, warnings, stats


def main():
    """Run validation and print results"""
    print("=" * 60)
    print("TAC ARCHITECTURE VALIDATION")
    print("=" * 60)
    print()
    
    # Load data
    data = load_pillars()
    
    # Run validation
    errors, warnings, stats = validate_pillars(data)
    
    # Print statistics
    print("📊 STATISTICS")
    print("-" * 40)
    print(f"   Pillars:        {stats['pillars']}")
    print(f"   Sub-Pillars:    {stats['sub_pillars']}")
    print(f"   Branches:       {stats['branches']}")
    print(f"   Topic Domains:  {stats['topic_domains']}")
    print()
    
    # Print errors
    if errors:
        print("❌ ERRORS (Must Fix)")
        print("-" * 40)
        for error in errors:
            print(f"   {error}")
        print()
    
    # Print warnings
    if warnings:
        print("⚠️  WARNINGS (Review Recommended)")
        print("-" * 40)
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    # Print summary
    print("=" * 60)
    if errors:
        print(f"❌ VALIDATION FAILED: {len(errors)} error(s) found")
        print("   Fix errors before committing!")
        return 1
    elif warnings:
        print(f"✅ VALIDATION PASSED with {len(warnings)} warning(s)")
        print("   Review warnings but OK to proceed")
        return 0
    else:
        print("✅ VALIDATION PASSED - No issues found!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
