# Playwright E2E Test Plan

End-to-end tests for OAuth credentials UI

## Test Files (3 files)

### credentials-ui.spec.js
**Purpose**: Verify UI elements and navigation

**Tests**:
1. `test_settings_tab_shows_credentials_section` - Section visible
2. `test_credentials_section_has_heading` - Proper heading
3. `test_google_provider_card_visible` - Google card rendered
4. `test_microsoft_provider_card_visible` - Microsoft card rendered
5. `test_icloud_info_panel_visible` - iCloud info shown
6. `test_provider_status_badges_visible` - Status badges present
7. `test_configure_buttons_clickable` - Buttons are enabled

**Setup**: Navigate to Settings tab

### credentials-forms.spec.js
**Purpose**: Test form interactions

**Tests**:
1. `test_click_configure_shows_form` - Form appears on click
2. `test_google_form_has_required_fields` - Client ID/Secret fields
3. `test_microsoft_form_has_required_fields` - All 3 fields
4. `test_form_validation_on_empty_submit` - Validation messages
5. `test_cancel_button_hides_form` - Cancel works
6. `test_form_input_accepts_text` - Fields accept input
7. `test_save_button_enabled_with_data` - Save enabled

**Setup**: Navigate to Settings, click Configure

### credentials-visual.spec.js
**Purpose**: Visual validation

**Tests**:
1. `test_provider_cards_proper_spacing` - CSS layout correct
2. `test_status_badges_color_coding` - Configured vs not
3. `test_configured_credentials_display` - Masked values shown
4. `test_form_styling_matches_theme` - Consistent styling
5. `test_help_links_present` - Setup guide links visible
6. `test_dark_mode_credentials_section` - Dark theme works

**Setup**: Multiple theme/state scenarios

## Prerequisites
- Server running on localhost:3000
- Test database with sample data
- Clean state between tests

## Coverage Target: 80%+
