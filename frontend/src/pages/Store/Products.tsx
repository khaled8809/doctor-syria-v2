import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  TextField,
  MenuItem,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Rating,
  Stack,
  Alert,
  InputAdornment,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Divider,
  FormControlLabel,
  Switch,
} from '@mui/material';
import {
  Search as SearchIcon,
  ShoppingCart as CartIcon,
  FilterList as FilterIcon,
  LocalHospital as PrescriptionIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import axios from 'axios';
import { useSnackbar } from 'notistack';
import { format } from 'date-fns';

const CATEGORIES = [
  { value: 'MEDICATION', label: 'Medication' },
  { value: 'EQUIPMENT', label: 'Medical Equipment' },
  { value: 'SUPPLIES', label: 'Medical Supplies' },
  { value: 'INSTRUMENTS', label: 'Medical Instruments' },
];

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  image_url: string;
  is_available: boolean;
  requires_prescription: boolean;
  min_order_quantity: number;
  max_order_quantity: number | null;
  reviews: Review[];
}

interface Review {
  id: number;
  user: {
    id: number;
    name: string;
  };
  rating: number;
  comment: string;
  created_at: string;
}

const Products = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [showPrescriptionOnly, setShowPrescriptionOnly] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [prescriptionFile, setPrescriptionFile] = useState<File | null>(null);
  const [filterDrawerOpen, setFilterDrawerOpen] = useState(false);
  const [productDialogOpen, setProductDialogOpen] = useState(false);

  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  // Fetch products
  const { data: products, isLoading } = useQuery(
    ['products', searchQuery, selectedCategory, minPrice, maxPrice, showPrescriptionOnly],
    () =>
      axios
        .get('/api/store/products/', {
          params: {
            search: searchQuery,
            category: selectedCategory,
            min_price: minPrice,
            max_price: maxPrice,
            requires_prescription: showPrescriptionOnly || undefined,
          },
        })
        .then((res) => res.data)
  );

  // Add to cart mutation
  const addToCartMutation = useMutation(
    (data: FormData) => axios.post('/api/store/cart/add/', data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('cart');
        handleCloseProductDialog();
        enqueueSnackbar('Product added to cart', { variant: 'success' });
      },
      onError: (error: any) => {
        enqueueSnackbar(error.response?.data?.message || 'Error adding to cart', {
          variant: 'error',
        });
      },
    }
  );

  const handleOpenProductDialog = (product: Product) => {
    setSelectedProduct(product);
    setQuantity(product.min_order_quantity);
    setPrescriptionFile(null);
    setProductDialogOpen(true);
  };

  const handleCloseProductDialog = () => {
    setProductDialogOpen(false);
    setSelectedProduct(null);
    setQuantity(1);
    setPrescriptionFile(null);
  };

  const handleAddToCart = () => {
    if (!selectedProduct) return;

    const formData = new FormData();
    formData.append('product_id', selectedProduct.id.toString());
    formData.append('quantity', quantity.toString());
    if (prescriptionFile) {
      formData.append('prescription', prescriptionFile);
    }

    addToCartMutation.mutate(formData);
  };

  const handlePrescriptionUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setPrescriptionFile(event.target.files[0]);
    }
  };

  const getAverageRating = (reviews: Review[]) => {
    if (!reviews.length) return 0;
    return (
      reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length
    );
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Search and Filter Bar */}
      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search products..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
        <Button
          variant="outlined"
          startIcon={<FilterIcon />}
          onClick={() => setFilterDrawerOpen(true)}
        >
          Filters
        </Button>
      </Stack>

      {/* Product Grid */}
      <Grid container spacing={3}>
        {(products || []).map((product: Product) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
            <Card>
              <CardMedia
                component="img"
                height="200"
                image={product.image_url || '/placeholder.png'}
                alt={product.name}
              />
              <CardContent>
                <Typography gutterBottom variant="h6" component="div">
                  {product.name}
                </Typography>
                <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
                  <Chip
                    label={
                      CATEGORIES.find((c) => c.value === product.category)?.label
                    }
                    size="small"
                  />
                  {product.requires_prescription && (
                    <Chip
                      icon={<PrescriptionIcon />}
                      label="Prescription Required"
                      size="small"
                      color="warning"
                    />
                  )}
                </Stack>
                <Typography variant="body2" color="text.secondary" noWrap>
                  {product.description}
                </Typography>
                <Box sx={{ mt: 2, mb: 1 }}>
                  <Rating
                    value={getAverageRating(product.reviews)}
                    readOnly
                    size="small"
                  />
                  <Typography variant="caption" sx={{ ml: 1 }}>
                    ({product.reviews.length} reviews)
                  </Typography>
                </Box>
                <Typography variant="h6" color="primary" sx={{ mb: 1 }}>
                  ${product.price.toFixed(2)}
                </Typography>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<CartIcon />}
                  onClick={() => handleOpenProductDialog(product)}
                  disabled={!product.is_available}
                >
                  {product.is_available ? 'Add to Cart' : 'Out of Stock'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Filter Drawer */}
      <Drawer
        anchor="right"
        open={filterDrawerOpen}
        onClose={() => setFilterDrawerOpen(false)}
      >
        <Box sx={{ width: 300, p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Filters
          </Typography>
          <List>
            <ListItem>
              <TextField
                fullWidth
                select
                label="Category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <MenuItem value="">All Categories</MenuItem>
                {CATEGORIES.map((category) => (
                  <MenuItem key={category.value} value={category.value}>
                    {category.label}
                  </MenuItem>
                ))}
              </TextField>
            </ListItem>
            <ListItem>
              <TextField
                fullWidth
                label="Minimum Price"
                type="number"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
              />
            </ListItem>
            <ListItem>
              <TextField
                fullWidth
                label="Maximum Price"
                type="number"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
              />
            </ListItem>
            <ListItem>
              <FormControlLabel
                control={
                  <Switch
                    checked={showPrescriptionOnly}
                    onChange={(e) => setShowPrescriptionOnly(e.target.checked)}
                  />
                }
                label="Prescription Items Only"
              />
            </ListItem>
          </List>
        </Box>
      </Drawer>

      {/* Product Dialog */}
      <Dialog
        open={productDialogOpen}
        onClose={handleCloseProductDialog}
        maxWidth="sm"
        fullWidth
      >
        {selectedProduct && (
          <>
            <DialogTitle>{selectedProduct.name}</DialogTitle>
            <DialogContent>
              <Box sx={{ mb: 2 }}>
                <img
                  src={selectedProduct.image_url || '/placeholder.png'}
                  alt={selectedProduct.name}
                  style={{ width: '100%', maxHeight: 300, objectFit: 'contain' }}
                />
              </Box>
              <Typography>{selectedProduct.description}</Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="h6" color="primary">
                  ${selectedProduct.price.toFixed(2)}
                </Typography>
              </Box>
              {selectedProduct.requires_prescription && (
                <Alert severity="warning" sx={{ mt: 2 }}>
                  This product requires a valid prescription
                </Alert>
              )}
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Quantity"
                    value={quantity}
                    onChange={(e) => setQuantity(Number(e.target.value))}
                    inputProps={{
                      min: selectedProduct.min_order_quantity,
                      max: selectedProduct.max_order_quantity || undefined,
                    }}
                  />
                </Grid>
                {selectedProduct.requires_prescription && (
                  <Grid item xs={12}>
                    <Button
                      variant="outlined"
                      component="label"
                      fullWidth
                    >
                      Upload Prescription
                      <input
                        type="file"
                        hidden
                        accept="image/*,.pdf"
                        onChange={handlePrescriptionUpload}
                      />
                    </Button>
                    {prescriptionFile && (
                      <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                        Selected file: {prescriptionFile.name}
                      </Typography>
                    )}
                  </Grid>
                )}
              </Grid>
              {selectedProduct.reviews.length > 0 && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    Reviews
                  </Typography>
                  <List>
                    {selectedProduct.reviews.map((review) => (
                      <React.Fragment key={review.id}>
                        <ListItem alignItems="flex-start">
                          <ListItemText
                            primary={
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Rating
                                  value={review.rating}
                                  readOnly
                                  size="small"
                                />
                                <Typography
                                  variant="caption"
                                  sx={{ ml: 1 }}
                                  color="text.secondary"
                                >
                                  {format(
                                    new Date(review.created_at),
                                    'MMM d, yyyy'
                                  )}
                                </Typography>
                              </Box>
                            }
                            secondary={
                              <>
                                <Typography
                                  variant="body2"
                                  color="text.primary"
                                  sx={{ my: 1 }}
                                >
                                  {review.comment}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  By {review.user.name}
                                </Typography>
                              </>
                            }
                          />
                        </ListItem>
                        <Divider />
                      </React.Fragment>
                    ))}
                  </List>
                </Box>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseProductDialog}>Cancel</Button>
              <Button
                variant="contained"
                onClick={handleAddToCart}
                disabled={
                  addToCartMutation.isLoading ||
                  (selectedProduct.requires_prescription && !prescriptionFile)
                }
              >
                Add to Cart
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default Products;
