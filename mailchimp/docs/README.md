# Mailchimp Templates for Bathroom Trade Hub

This folder contains Mailchimp email templates for displaying dynamic customer segment discounts.

## 📁 Folder Structure

```
mailchimp/
├── templates/          # HTML email templates
├── assets/            # Images, logos, and other assets
└── docs/             # Documentation and guides
```

## 🎨 Available Templates

### 1. **discount-table-styled.html**

- **Use Case**: Premium styled discount table with gradients and animations
- **Features**:
  - Modern CSS styling with gradients
  - Hover effects and premium badges
  - Mobile responsive design
  - Customer status footer
- **Best For**: Newsletter campaigns, promotional emails

### 2. **discount-table-simple.html**

- **Use Case**: Simple, compatible table design
- **Features**:
  - Basic styling for maximum email client compatibility
  - Clean, professional appearance
  - Lightweight code
- **Best For**: Automated emails, transactional messages

### 3. **discount-cards.html**

- **Use Case**: Modern card-based layout
- **Features**:
  - Individual cards for each collection
  - Visual badges and labels
  - Flexible grid layout
  - Call-to-action sections
- **Best For**: Product showcase emails, seasonal campaigns

## 🔧 Implementation Guide

### Step 1: Choose Your Template

Select the appropriate template based on your email campaign needs.

### Step 2: Copy to Mailchimp

1. Open your chosen template file
2. Copy the entire HTML content
3. In Mailchimp, create a new email campaign
4. Switch to "Code" view (not visual editor)
5. Paste the template code

### Step 3: Customize Content

- Replace placeholder text with your content
- Update product collection names if needed
- Modify discount percentages to match current offers
- Adjust colors to match your brand

### Step 4: Test Before Sending

- Use Mailchimp's preview feature
- Send test emails to different customer segments
- Verify conditional content displays correctly

## 🎯 Mailchimp Merge Tags Used

### Customer Segmentation

- `*|IF:TAGS contains 'hubpro'|*` - HubPRO members (free + plus)
- `*|IF:TAGS contains 'hubpro-plus'|*` - HubPRO+ members only
- `*|IF:TAGS contains 'hubpro-free'|*` - HubPRO free members only
- `*|IF:TAGS contains 'diy'|*` - DIY customers

### Discount Structure

Based on your Shopify discount setup:

**HubPRO Members:**

- Kartell: 45% OFF
- Scudo: 45% OFF
- Maxi Panels: 50% OFF
- VIVA: 35% OFF
- HubChoice: 35% OFF

**DIY Customers:**

- Kartell: 35% OFF
- Scudo: 30% OFF
- Maxi Panels: 35% OFF
- VIVA: 15% OFF
- HubChoice: 25% OFF

## 🚨 Important Notes

### Email Client Compatibility

- **Styled Template**: Works best in modern email clients (Gmail, Outlook 365, Apple Mail)
- **Simple Template**: Compatible with all email clients including older versions
- **Cards Template**: May have limited support in older email clients

### Mailchimp Best Practices

1. **Always use Code view** when pasting templates
2. **Don't switch to visual editor** after pasting code
3. **Test with real customer data** before sending
4. **Use "Send Test Email"** to verify conditional content

### Troubleshooting

- If merge tags show as literal text, ensure you're in Code view
- Verify customer tags are properly synced from Shopify
- Check that tag names match exactly (case-sensitive)
- Use Mailchimp's merge tag tester for debugging

## 🔄 Updating Templates

### When Discount Percentages Change

1. Update the percentages in the template files
2. Update this README with new discount structure
3. Test the updated templates before using in campaigns

### When Adding New Collections

1. Add new table rows or cards to templates
2. Include appropriate conditional logic
3. Update the discount structure documentation

## 📞 Support

For questions about these templates or Mailchimp integration:

1. Check Mailchimp's merge tag documentation
2. Test templates with sample customer data
3. Verify Shopify-Mailchimp integration is working

---

**Last Updated**: [Current Date]  
**Template Version**: 1.0  
**Compatible with**: Mailchimp Standard & Premium plans
