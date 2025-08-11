# Mailchimp Implementation Guide

## Dynamic Discount Display for Customer Segments

### 🎯 Quick Start

**Copy this code into your Mailchimp email (Code view only):**

```html
<table
  style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;"
>
  <tr style="background-color: #2c3e50;">
    <th style="color: white; padding: 15px; text-align: left;">
      Product Collection
    </th>
    <th style="color: white; padding: 15px; text-align: center;">
      Your Discount
    </th>
  </tr>
  <tr>
    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">
      <strong>Kartell Collection</strong><br /><span
        style="color: #6c757d; font-size: 14px;"
        >Premium bathroom fixtures</span
      >
    </td>
    <td
      style="padding: 12px; border-bottom: 1px solid #dee2e6; text-align: center;"
    >
      *|IF:TAGS contains 'hubpro'|*<span
        style="background-color: #dc3545; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
        >45% OFF</span
      >*|ELSE:|*<span
        style="background-color: #28a745; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
        >35% OFF</span
      >*|END:IF|*
    </td>
  </tr>
  <tr>
    <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">
      <strong>Maxi Panels Collection</strong><br /><span
        style="color: #6c757d; font-size: 14px;"
        >Premium wall panels</span
      >
    </td>
    <td
      style="padding: 12px; border-bottom: 1px solid #dee2e6; text-align: center;"
    >
      *|IF:TAGS contains 'hubpro'|*<span
        style="background-color: #dc3545; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
        >50% OFF</span
      >*|ELSE:|*<span
        style="background-color: #28a745; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
        >35% OFF</span
      >*|END:IF|*
    </td>
  </tr>
  <tr>
    <td style="padding: 12px;">
      <strong>Scudo Collection</strong><br /><span
        style="color: #6c757d; font-size: 14px;"
        >Quality bathroom suites</span
      >
    </td>
    <td style="padding: 12px; text-align: center;">
      *|IF:TAGS contains 'hubpro'|*<span
        style="background-color: #dc3545; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
        >45% OFF</span
      >*|ELSE:|*<span
        style="background-color: #28a745; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
        >30% OFF</span
      >*|END:IF|*
    </td>
  </tr>
</table>
```

### 📋 Step-by-Step Instructions

#### 1. Create New Email Campaign

- Go to Mailchimp → Campaigns → Create Campaign
- Choose "Email" → "Regular" campaign
- Select your audience

#### 2. Design Your Email

- Choose "Code your own" template
- Click "Code" tab (important!)
- Paste one of the template codes

#### 3. Add Dynamic Content

- The templates automatically show different discounts based on customer tags
- HubPRO members see higher discounts (red badges)
- DIY customers see standard discounts (green badges)

#### 4. Test Your Email

- Use "Preview and Test" → "Send a Test Email"
- Test with customers who have different tags
- Verify discounts display correctly

### 🔧 Customization Options

#### Change Discount Percentages

Find this part in the code:

```html
*|IF:TAGS contains 'hubpro'|*45% OFF*|ELSE:|*35% OFF*|END:IF|*
```

Change the percentages to match your current offers.

#### Add New Product Collections

Copy this row structure and modify:

```html
<tr>
  <td style="padding: 12px; border-bottom: 1px solid #dee2e6;">
    <strong>NEW COLLECTION NAME</strong><br />
    <span style="color: #6c757d; font-size: 14px;">Collection description</span>
  </td>
  <td
    style="padding: 12px; border-bottom: 1px solid #dee2e6; text-align: center;"
  >
    *|IF:TAGS contains 'hubpro'|*<span
      style="background-color: #dc3545; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
      >XX% OFF</span
    >*|ELSE:|*<span
      style="background-color: #28a745; color: white; padding: 6px 12px; border-radius: 15px; font-weight: bold;"
      >XX% OFF</span
    >*|END:IF|*
  </td>
</tr>
```

#### Modify Colors

- **HubPRO badges (red)**: Change `#dc3545` to your preferred color
- **DIY badges (green)**: Change `#28a745` to your preferred color
- **Header background**: Change `#2c3e50` to your brand color

### 🚨 Common Issues & Solutions

#### Issue: Merge tags show as literal text

**Solution**: Make sure you're using the "Code" view, not the visual editor.

#### Issue: All customers see the same discount

**Solution**:

1. Check that customer tags are syncing from Shopify
2. Verify tag names match exactly (`hubpro-free`, `hubpro-plus`, `diy`)
3. Test with customers who actually have these tags

#### Issue: Email looks broken in some clients

**Solution**: Use the "Simple" template version for better compatibility.

### 📊 Testing Checklist

- [ ] Copy template to Mailchimp (Code view only)
- [ ] Preview email in desktop view
- [ ] Preview email in mobile view
- [ ] Send test to HubPRO customer
- [ ] Send test to DIY customer
- [ ] Send test to customer with no tags
- [ ] Verify correct discounts display for each segment
- [ ] Check all links work properly

### 🎨 Template Variations

#### For Simple Compatibility

Use `discount-table-simple.html` - works in all email clients

#### For Modern Design

Use `discount-table-styled.html` - includes gradients and animations

#### For Product Showcase

Use `discount-cards.html` - card-based layout with visual appeal

### 📈 Best Practices

1. **Test Before Sending**: Always preview with real customer data
2. **Keep It Simple**: Avoid complex CSS for better email client support
3. **Mobile First**: Test on mobile devices - most emails are opened on mobile
4. **Update Regularly**: Keep discount percentages current with your Shopify setup
5. **Segment Your Audience**: Send targeted campaigns to specific customer groups

### 🔄 Maintenance

#### Monthly Tasks

- [ ] Verify discount percentages match Shopify
- [ ] Test templates with new customers
- [ ] Update product collection descriptions if needed

#### When Shopify Discounts Change

1. Update percentages in template files
2. Test updated templates
3. Update any active email campaigns
4. Document changes in this guide

---

**Need Help?** Check the main README.md file for detailed documentation and troubleshooting tips.
