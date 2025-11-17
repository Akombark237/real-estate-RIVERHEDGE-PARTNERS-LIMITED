# About Page Editor - User Guide
## RIVERHEDGE PARTNERS LIMITED Real Estate Platform

---

## 🎯 Overview

The About Page Editor allows **ADMIN USERS ONLY** to edit all content on the About page without touching any code. This includes:
- Company description
- Mission and vision statements
- Core values
- Services offered
- Contact information
- Social media links
- Statistics (years of experience, properties sold, etc.)
- Team information

---

## 🔐 Access Control

### Who Can Edit?
- **ADMIN USERS ONLY** (users with `is_staff = True`)
- Regular users can only VIEW the About page
- Only admins see the "Edit About Page" button

### How to Make a User Admin:
1. Go to Django Admin: http://localhost:8000/admin/
2. Navigate to **Users**
3. Click on the user you want to make admin
4. Check the **"Staff status"** checkbox
5. Save

---

## 📝 How to Edit the About Page

### Step 1: Login as Admin
1. Login to the platform with an admin account
2. Navigate to the **About** page from the menu

### Step 2: Access the Editor
1. On the About page, you'll see an **"Edit About Page"** button (top right)
2. Click the button to open the editor

### Step 3: Edit Content
The editor is organized into sections:

#### **Page Header**
- **Title**: Main heading (e.g., "About RIVERHEDGE PARTNERS LIMITED")
- **Subtitle**: Tagline or short description

#### **Company Information**
- **Company Description**: Main overview of your company
- **Mission Statement**: Your company's mission
- **Vision Statement**: Your company's vision

#### **Core Values & Services**
- **Core Values**: Enter one value per line
  ```
  Integrity
  Excellence
  Innovation
  Customer Focus
  ```
- **Services**: Enter one service per line
  ```
  Property Development
  Real Estate Consulting
  Investment Advisory
  ```

#### **Contact Information**
- Email address
- Phone number
- Physical address

#### **Social Media Links**
- Facebook URL
- Twitter URL
- LinkedIn URL
- Instagram URL

#### **Additional Content**
- **Why Choose Us**: Explain what makes your company special
- **Team Description**: Brief description of your team

#### **Statistics**
- Years of Experience
- Properties Sold
- Happy Clients
- Team Members

### Step 4: Save Changes
1. Review your changes
2. Click **"Save Changes"** button at the bottom
3. You'll see a success message when saved
4. Click **"Preview About Page"** to see your changes live

---

## 🎨 Features

### ✅ What You Can Do:
- Edit all text content on the About page
- Update contact information
- Change social media links
- Update statistics
- Add/remove core values and services
- Preview changes before publishing

### ❌ What You Cannot Do:
- Change the page layout or design
- Add images (currently text-only)
- Delete the About page
- Create multiple About pages (only one exists)

---

## 🔧 Technical Details

### Backend (Django)
- **App**: `pages`
- **Model**: `AboutPage` (singleton pattern - only one instance)
- **Admin Interface**: Available at `/admin/pages/aboutpage/`
- **API Endpoint**: `/api/pages/about/`

### Frontend (React)
- **View Page**: `/about`
- **Edit Page**: `/about/edit` (admin only)
- **Components**:
  - `About.jsx` - Public view
  - `AboutEditor.jsx` - Admin editor

### Database
- Table: `pages_aboutpage`
- Tracks who last updated and when
- Stores all content in one record

---

## 📋 Admin Panel Alternative

You can also edit the About page through Django Admin:

1. Go to: http://localhost:8000/admin/
2. Click on **"Pages"** → **"About Page"**
3. Edit the content
4. Click **"Save"**

**Note**: The frontend editor is more user-friendly, but Django Admin gives you more control.

---

## 🎯 Best Practices

### Content Guidelines:
1. **Keep it concise**: Users prefer shorter, impactful content
2. **Use clear language**: Avoid jargon
3. **Update regularly**: Keep statistics current
4. **Proofread**: Check for typos before saving
5. **Test links**: Verify social media URLs work

### Core Values:
- Limit to 5-12 values (too many dilutes impact)
- Use single words or short phrases
- Make them memorable and meaningful

### Services:
- List 4-8 main services
- Be specific but concise
- Focus on what makes you unique

### Statistics:
- Update quarterly or annually
- Use realistic numbers
- Round to nice numbers (e.g., 100+ instead of 97)

---

## 🚀 Quick Start Checklist

- [ ] Login as admin user
- [ ] Navigate to About page
- [ ] Click "Edit About Page" button
- [ ] Update company description
- [ ] Update mission and vision
- [ ] Add/edit core values (one per line)
- [ ] Add/edit services (one per line)
- [ ] Update contact information
- [ ] Add social media links
- [ ] Update statistics
- [ ] Click "Save Changes"
- [ ] Preview the About page
- [ ] Verify all changes look correct

---

## 🔍 Troubleshooting

### "Edit About Page" button not showing?
- **Solution**: Make sure you're logged in as an admin user (is_staff = True)

### Changes not saving?
- **Solution**: Check your internet connection and try again
- **Solution**: Make sure you're still logged in (token may have expired)

### Error message when saving?
- **Solution**: Check that URLs are valid (must start with http:// or https://)
- **Solution**: Check that email is in valid format

### Can't access /about/edit?
- **Solution**: Only admin users can access this page
- **Solution**: You'll be redirected to dashboard if not admin

---

## 📞 Support

### For Technical Issues:
- Check browser console for errors (F12)
- Check Django logs in terminal
- Verify database migrations are up to date

### For Content Questions:
- Review existing content for examples
- Keep backups of important content
- Test changes in a staging environment first

---

## 🎓 Example Content

### Good Company Description:
```
RIVERHEDGE PARTNERS LIMITED is a leading real estate and investment 
company based in Abuja, Nigeria. We specialize in providing affordable 
housing solutions, property development, and real estate investment 
advisory services for middle-income families. With over 5 years of 
experience, we've helped hundreds of families achieve their dream of 
homeownership.
```

### Good Mission Statement:
```
To make quality homeownership accessible and affordable for middle-income 
families by creating vibrant, sustainable communities with well-designed, 
value-driven homes that meet the needs of modern living.
```

### Good Core Values (one per line):
```
Integrity
Affordability
Efficiency
Timely Delivery
Customer Commitment
Innovation
Excellence
```

---

## 🔄 Update History

The system automatically tracks:
- **Last Updated**: Date and time of last change
- **Updated By**: Which admin user made the change

You can see this information in the Django Admin panel.

---

## ✨ Future Enhancements

Planned features:
- [ ] Image upload for company logo
- [ ] Team member photos
- [ ] Rich text editor (bold, italic, lists)
- [ ] Multiple language support
- [ ] Version history / rollback
- [ ] Preview mode before publishing

---

## 📝 Summary

The About Page Editor gives you complete control over your company's About page content without needing to edit code. Simply login as an admin, click "Edit About Page", make your changes, and save. Your changes appear immediately on the live site.

**Remember**: Only admin users can edit. Regular users can only view the About page.

---

**Happy Editing! 🎉**

